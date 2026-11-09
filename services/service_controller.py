'''
Service Controller - Manages MySQL, PHP, and phpMyAdmin services
Thread-safe service management with status updates
'''
import os
import sys
import subprocess
import shutil
import time
import socket
import platform
import threading
import queue
from pathlib import Path
from typing import Optional, Callable, Dict, Any, Tuple
from enum import Enum

class ServiceStatus(Enum):
    '''Service status enumeration'''
    STOPPED = 'stopped'
    RUNNING = 'running'
    ERROR = 'error'
    STARTING = 'starting'
    STOPPING = 'stopping'


class ServiceController:
    '''Main service controller for MySQL, PHP, and phpMyAdmin'''
    
    def __init__(self, base_dir, status_callback = None):
        '''
Initialize ServiceController

Args:
    base_dir: Base directory of the application
    status_callback: Optional callback for status updates
'''
        self.base_dir = base_dir.resolve()
        self.status_callback = status_callback
        self.log_queue = queue.Queue()
        self.mysql_status = ServiceStatus.STOPPED
        self.php_status = ServiceStatus.STOPPED
        self.mysql_process = None
        self.php_process = None
        self.mysql_dir = self.base_dir / 'MySQL Server 9.5'
        self.mysql_bin = self.mysql_dir / 'bin'
        self.mysql_exe = self.mysql_bin / 'mysqld.exe'
        self.my_ini = self.mysql_dir / 'my.ini'
        self.data_dir = self.base_dir / 'data'
        self.php_dir = self.base_dir / 'php'
        self.php_exe = self.php_dir / 'php.exe'
        self.pma_dir = self.base_dir / 'phpMyAdmin-5.2.3-all-languages'
        self.config_file = self.pma_dir / 'config.inc.php'
        self.mysql_port = 3306
        self.php_port = 8080

    
    def log(self, message, level = 'INFO'):
        '''Add log message to queue'''
        timestamp = time.strftime('%H:%M:%S')
        self.log_queue.put(f'''[{timestamp}] [{level}] {message}''')

    
    def check_port_listening(self, port):
        """Check if port is listening (supports both IPv4 and IPv6)"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex(('127.0.0.1', port))
                if result == 0:
                    return True
        except:
            pass

        try:
            with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex(('::1', port))
                if result == 0:
                    return True
        except:
            pass

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex(('localhost', port))
                return result == 0
        except:
            return False

    
    def check_mysql_running(self):
        '''Check if MySQL is running'''
        
        try:
            result = subprocess.run([
                'tasklist',
                '/FI',
                'IMAGENAME eq mysqld.exe'], capture_output = True, text = True, timeout = 2, creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
            return 'mysqld.exe' in result.stdout
        except:
            return False


    
    def kill_process_on_port(self, port):
        '''Kill process on specified port'''
        
        try:
            result = subprocess.run([
                'netstat',
                '-ano'], capture_output = True, text = True, timeout = 2, creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
            for line in result.stdout.split('\n'):
                if not f''':{port}''' in line:
                    continue
                if not 'LISTENING' in line:
                    continue
                parts = line.split()
                if not len(parts) > 4:
                    continue
                pid = parts[-1]
                subprocess.run([
                    'taskkill',
                    '/F',
                    '/PID',
                    pid], capture_output = True, timeout = 2, creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
        except:
            return None


    
    def start_mysql(self):
        '''Start MySQL Server (non-blocking)'''
        
        def _start():
            
            try:
                self.mysql_status = ServiceStatus.STARTING
                if self.status_callback:
                    self.status_callback('mysql', ServiceStatus.STARTING)
                if not self.mysql_exe.exists():
                    self.log(f'''MySQL executable not found: {self.mysql_exe}''', 'ERROR')
                    self.mysql_status = ServiceStatus.ERROR
                    if self.status_callback:
                        self.status_callback('mysql', ServiceStatus.ERROR)
                    return None
                self.log('Starting MySQL Server...', 'INFO')
                self.update_my_ini()
                self.mysql_process = subprocess.Popen([
                    str(self.mysql_exe),
                    f'''--defaults-file={self.my_ini}'''], cwd = str(self.mysql_bin), stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
                max_wait_seconds = 30
                check_interval = 0.5
                max_iterations = int(max_wait_seconds / check_interval)
                for i in range(max_iterations):
                    time.sleep(check_interval)
                    if self.mysql_process.poll() is not None:
                        returncode = self.mysql_process.returncode
                        error_msg = f'''Process exited with code {returncode}''' if returncode else 'Process exited unexpectedly'
                        self.log(error_msg, 'ERROR')
                        self.mysql_status = ServiceStatus.ERROR
                        if self.status_callback:
                            self.status_callback('mysql', ServiceStatus.ERROR)
                        return None
                    if self.check_port_listening(self.mysql_port):
                        if self.check_mysql_running():
                            self.mysql_status = ServiceStatus.RUNNING
                            elapsed = i * check_interval
                            self.log(f'''MySQL Server started successfully (took {elapsed:.1f}s)''', 'SUCCESS')
                            if self.status_callback:
                                self.status_callback('mysql', ServiceStatus.RUNNING)
                            return None
                if self.check_mysql_running():
                    self.log('MySQL process is running, waiting for port to become ready...', 'INFO')
                    for _ in range(10):
                        time.sleep(0.5)
                        if self.check_port_listening(self.mysql_port):
                            self.mysql_status = ServiceStatus.RUNNING
                            self.log('MySQL Server started successfully (after extended wait)', 'SUCCESS')
                            if self.status_callback:
                                self.status_callback('mysql', ServiceStatus.RUNNING)
                            break
                    else:
                        self.mysql_status = ServiceStatus.ERROR
                        self.log(f'''MySQL Server start timeout after {max_wait_seconds}s''', 'ERROR')
                        if self.status_callback:
                            self.status_callback('mysql', ServiceStatus.ERROR)
            except Exception as e:
                self.mysql_status = ServiceStatus.ERROR
                self.log(f'''Failed to start MySQL: {e}''', 'ERROR')
                if self.status_callback:
                    self.status_callback('mysql', ServiceStatus.ERROR)
                    return None
                return None


        thread = threading.Thread(target = _start, daemon = True)
        thread.start()
        return True

    
    def stop_mysql(self):
        '''Stop MySQL Server (non-blocking)'''
        
        def _stop():
            
            try:
                self.mysql_status = ServiceStatus.STOPPING
                if self.status_callback:
                    self.status_callback('mysql', ServiceStatus.STOPPING)
                self.log('Stopping MySQL Server...', 'INFO')
                if self.mysql_process:
                    
                    try:
                        self.mysql_process.terminate()
                        self.mysql_process.wait(timeout = 5)
                    except:
                        
                        try:
                            self.mysql_process.kill()
                        except:
                            pass


                
                try:
                    subprocess.run([
                        'taskkill',
                        '/F',
                        '/IM',
                        'mysqld.exe'], capture_output = True, timeout = 5, creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
                except:
                    pass

                time.sleep(2)
                self.mysql_status = ServiceStatus.STOPPED
                self.log('MySQL Server stopped', 'INFO')
                if self.status_callback:
                    self.status_callback('mysql', ServiceStatus.STOPPED)
                    return None
            except Exception as e:
                self.log(f'''Failed to stop MySQL: {e}''', 'ERROR')
                self.mysql_status = ServiceStatus.STOPPED
                if self.status_callback:
                    self.status_callback('mysql', ServiceStatus.STOPPED)
                    return None
                return None


        thread = threading.Thread(target = _stop, daemon = True)
        thread.start()
        return True

    
    def start_php(self):
        '''Start PHP Web Server (non-blocking)'''
        
        def _start():
            
            try:
                self.php_status = ServiceStatus.STARTING
                if self.status_callback:
                    self.status_callback('php', ServiceStatus.STARTING)
                if not self.php_exe.exists():
                    
                    try:
                        result = subprocess.run([
                            'php',
                            '-v'], capture_output = True, timeout = 2)
                        php_cmd = 'php'
                    except:
                        self.log('PHP not found', 'ERROR')
                        self.php_status = ServiceStatus.ERROR
                        if self.status_callback:
                            self.status_callback('php', ServiceStatus.ERROR)
                        return None

                else:
                    php_cmd = str(self.php_exe)
                if self.check_port_listening(self.php_port):
                    self.log(f'''Port {self.php_port} already in use, killing...''', 'WARNING')
                    self.kill_process_on_port(self.php_port)
                    time.sleep(1)
                self.log(f'''Starting PHP Web Server on port {self.php_port}...''', 'INFO')
                router_script = self.base_dir / 'router.php'
                if not router_script.exists():
                    self.log('Router script not found, creating router.php...', 'WARNING')
                    router_content = (self.base_dir / 'router.php').read_text(encoding = 'utf-8') if (self.base_dir / 'router.php').exists() else None
                    if not router_content:
                        router_content = '<?php\n/**\n * Router script for PHP Built-in Server\n * Routes /myadmin to phpMyAdmin directory\n */\n$uri = parse_url($_SERVER[\'REQUEST_URI\'], PHP_URL_PATH);\nif ($uri === false) {\n    $uri = \'/\';\n}\n\nif (strpos($uri, \'/myadmin\') !== 0) {\n    return false;\n}\n\nif (preg_match(\'#^/myadmin(.*)$#\', $uri, $matches)) {\n    $path = $matches[1];\n    if (empty($path)) {\n        header(\'Location: /myadmin/\');\n        exit;\n    }\n    $path = ltrim($path, \'/\');\n    if (empty($path)) {\n        $path = \'index.php\';\n    }\n    \n    $phpMyAdminPath = __DIR__ . \'/phpMyAdmin-5.2.3-all-languages/\' . $path;\n    \n    if (file_exists($phpMyAdminPath) && is_file($phpMyAdminPath)) {\n        if (preg_match(\'/\\.php$/\', $phpMyAdminPath)) {\n            chdir(dirname($phpMyAdminPath));\n            $_SERVER[\'SCRIPT_NAME\'] = \'/myadmin/\' . $path;\n            $_SERVER[\'PHP_SELF\'] = \'/myadmin/\' . $path;\n            require $phpMyAdminPath;\n            exit;\n        } else {\n            $ext = strtolower(pathinfo($phpMyAdminPath, PATHINFO_EXTENSION));\n            $mimeTypes = [\n                \'css\' => \'text/css\',\n                \'js\' => \'application/javascript\',\n                \'png\' => \'image/png\',\n                \'jpg\' => \'image/jpeg\',\n                \'jpeg\' => \'image/jpeg\',\n                \'gif\' => \'image/gif\',\n                \'svg\' => \'image/svg+xml\',\n                \'ico\' => \'image/x-icon\',\n                \'woff\' => \'font/woff\',\n                \'woff2\' => \'font/woff2\',\n                \'ttf\' => \'font/ttf\',\n                \'eot\' => \'application/vnd.ms-fontobject\',\n                \'json\' => \'application/json\',\n                \'xml\' => \'application/xml\',\n                \'txt\' => \'text/plain\',\n                \'html\' => \'text/html\',\n                \'htm\' => \'text/html\',\n            ];\n            $mimeType = $mimeTypes[$ext] ?? \'application/octet-stream\';\n            \n            $lastModified = filemtime($phpMyAdminPath);\n            $etag = md5_file($phpMyAdminPath);\n            \n            header(\'Content-Type: \' . $mimeType);\n            header(\'Content-Length: \' . filesize($phpMyAdminPath));\n            header(\'Cache-Control: public, max-age=3600\');\n            header(\'Last-Modified: \' . gmdate(\'D, d M Y H:i:s\', $lastModified) . \' GMT\');\n            header(\'ETag: "\' . $etag . \'"\');\n            \n            if (isset($_SERVER[\'HTTP_IF_MODIFIED_SINCE\']) || isset($_SERVER[\'HTTP_IF_NONE_MATCH\'])) {\n                if (isset($_SERVER[\'HTTP_IF_NONE_MATCH\']) && $_SERVER[\'HTTP_IF_NONE_MATCH\'] === \'"\' . $etag . \'"\') {\n                    http_response_code(304);\n                    exit;\n                }\n            }\n            \n            readfile($phpMyAdminPath);\n            exit;\n        }\n    } else {\n        if (is_dir($phpMyAdminPath)) {\n            $indexPath = $phpMyAdminPath . \'/index.php\';\n            if (file_exists($indexPath)) {\n                chdir($phpMyAdminPath);\n                $_SERVER[\'SCRIPT_NAME\'] = \'/myadmin/\' . rtrim($path, \'/\') . \'/index.php\';\n                $_SERVER[\'PHP_SELF\'] = \'/myadmin/\' . rtrim($path, \'/\') . \'/index.php\';\n                require $indexPath;\n                exit;\n            }\n        }\n        http_response_code(404);\n        echo "404 - File not found: /myadmin" . $path;\n        exit;\n    }\n}\nreturn false;\n'
                    router_script.write_text(router_content, encoding = 'utf-8')
                original_cwd = os.getcwd()
                
                try:
                    os.chdir(str(self.base_dir))
                    self.php_process = subprocess.Popen([
                        php_cmd,
                        '-S',
                        f'''localhost:{self.php_port}''',
                        str(router_script)], cwd = str(self.base_dir), stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
                    os.chdir(original_cwd)
                except Exception as e:
                    os.chdir(original_cwd)
                    raise e

                max_checks = 10
                check_interval = 0.5
                server_started = False
                for i in range(max_checks):
                    time.sleep(check_interval)
                    if self.php_process.poll() is not None:
                        returncode = self.php_process.returncode
                        error_msg = f'''PHP process exited with code {returncode}''' if returncode else 'PHP process exited unexpectedly'
                        self.log(error_msg, 'ERROR')
                        break
                    if self.check_port_listening(self.php_port):
                        server_started = True
                        break
                if server_started:
                    self.php_status = ServiceStatus.RUNNING
                    self.log(f'''PHP Web Server started on http://localhost:{self.php_port}''', 'SUCCESS')
                    if self.status_callback:
                        self.status_callback('php', ServiceStatus.RUNNING)
                        return None
                    return None
                self.php_status = ServiceStatus.ERROR
                error_msg = 'PHP Web Server start failed'
                self.log(error_msg, 'ERROR')
                if self.status_callback:
                    self.status_callback('php', ServiceStatus.ERROR)
                    return None
            except Exception as e:
                self.php_status = ServiceStatus.ERROR
                self.log(f'''Failed to start PHP: {e}''', 'ERROR')
                if self.status_callback:
                    self.status_callback('php', ServiceStatus.ERROR)
                    return None
                return None


        thread = threading.Thread(target = _start, daemon = True)
        thread.start()
        return True

    
    def stop_php(self):
        '''Stop PHP Web Server (non-blocking)'''
        
        def _stop():
            
            try:
                self.php_status = ServiceStatus.STOPPING
                if self.status_callback:
                    self.status_callback('php', ServiceStatus.STOPPING)
                self.log('Stopping PHP Web Server...', 'INFO')
                if self.php_process:
                    
                    try:
                        self.php_process.terminate()
                        self.php_process.wait(timeout = 3)
                    except:
                        
                        try:
                            self.php_process.kill()
                        except:
                            pass


                if self.check_port_listening(self.php_port):
                    self.kill_process_on_port(self.php_port)
                time.sleep(1)
                self.php_status = ServiceStatus.STOPPED
                self.log('PHP Web Server stopped', 'INFO')
                if self.status_callback:
                    self.status_callback('php', ServiceStatus.STOPPED)
                    return None
            except Exception as e:
                self.log(f'''Failed to stop PHP: {e}''', 'ERROR')
                self.php_status = ServiceStatus.STOPPED
                if self.status_callback:
                    self.status_callback('php', ServiceStatus.STOPPED)
                    return None
                return None


        thread = threading.Thread(target = _stop, daemon = True)
        thread.start()
        return True

    
    def start_phpmyadmin(self):
        '''Start phpMyAdmin (MySQL + PHP Web Server)'''
        self.log('Starting phpMyAdmin...', 'INFO')
        if not self.check_mysql_running():
            self.start_mysql()
            time.sleep(5)
        if not self.config_file.exists():
            self.create_phpmyadmin_config()
        self.start_php()
        return True

    
    def stop_all(self):
        '''Stop all services'''
        self.log('Stopping all services...', 'INFO')
        self.stop_php()
        self.stop_mysql()

    
    def update_my_ini(self):
        '''Update my.ini with current paths'''
        mysql_dir_forward = str(self.mysql_dir).replace('\\', '/')
        data_dir_forward = str(self.data_dir).replace('\\', '/')
        share_dir = self.mysql_dir / 'share'
        share_dir_forward = str(share_dir).replace('\\', '/')
        content = f'''[mysqld]\n# Đường dẫn thư mục gốc\nbasedir={mysql_dir_forward}\ndatadir={data_dir_forward}\n\n# Đường dẫn messages\nlc-messages-dir={share_dir_forward}\n\n# Cổng kết nối\nport={self.mysql_port}\n\n# Cho phép truy cập từ xa\nbind-address=0.0.0.0\n\n# Mã hóa ký tự mặc định\ncharacter-set-server=utf8mb4\ncollation-server=utf8mb4_unicode_ci\n\n# Bật log error\nlog-error="mysql-error.log"\n\n# Không cần service\nskip-networking=0\n'''
        self.my_ini.write_text(content, encoding = 'utf-8')

    
    def create_phpmyadmin_config(self):
        '''Create phpMyAdmin config.inc.php'''
        content = "<?php\ndeclare(strict_types=1);\n\n// Blowfish secret for cookie authentication\n$cfg['blowfish_secret'] = 'phpMyAdmin2024SecretKey12345678';\n\n// Server configuration\n$i = 0;\n$i++;\n$cfg['Servers'][$i]['auth_type'] = 'cookie';\n$cfg['Servers'][$i]['host'] = 'localhost';\n$cfg['Servers'][$i]['port'] = '3306';\n$cfg['Servers'][$i]['compress'] = false;\n$cfg['Servers'][$i]['AllowNoPassword'] = true;\n\n// Directories for saving/loading files\n$cfg['UploadDir'] = '';\n$cfg['SaveDir'] = '';\n\n// Default language\n$cfg['DefaultLang'] = 'vi';\n\n// Increase timeout for large imports\n$cfg['ExecTimeLimit'] = 600;\n"
        self.config_file.write_text(content, encoding = 'utf-8')

    
    def check_php_installed(self):
        '''Check if PHP is installed'''
        if self.php_exe.exists():
            
            try:
                result = subprocess.run([
                    str(self.php_exe),
                    '-v'], capture_output = True, text = True, timeout = 3, errors = 'ignore')
                output = result.stdout if result.stdout else result.stderr
                for line in output.split('\n'):
                    if not 'PHP' in line:
                        continue
                    if not any(( char.isdigit() for char in line )):
                        continue
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if not part == 'PHP':
                            continue
                        if not i + 1 < len(parts):
                            continue
                        version = parts[i + 1]
                        if not version[0].isdigit():
                            continue
                        return (True, version.split()[0] if version else parts[i + 1])
                    for part in parts:
                        if not '.' in part:
                            continue
                        if not part.replace('.', '').replace('-', '').isdigit():
                            continue
                        return (True, part.split('-')[0].split('(')[0])
                return (True, 'Installed')
            except Exception as e:
                self.log(f'''Error checking PHP version: {e}''', 'WARNING')
                return (True, 'Unknown')

        
        try:
            result = subprocess.run([
                'php',
                '-v'], capture_output = True, text = True, timeout = 3)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if not 'PHP' in line:
                        continue
                    parts = line.split()
                    if not len(parts) > 1:
                        continue
                    return (True, parts[1])
                return (True, 'System')
        except:
            return (False, '')

        return (False, '')

    
    def refresh_status(self, silent = False):
        """
Refresh all service statuses

Args:
    silent: If True, don't log refresh actions (for periodic updates)
"""
        if not silent:
            self.log('Refreshing service statuses...', 'INFO')
        mysql_running = self.check_mysql_running()
        new_mysql_status = ServiceStatus.RUNNING if mysql_running else ServiceStatus.STOPPED
        if new_mysql_status != self.mysql_status:
            self.mysql_status = new_mysql_status
            if self.status_callback:
                self.status_callback('mysql', self.mysql_status)
        php_running = self.check_port_listening(self.php_port)
        new_php_status = ServiceStatus.RUNNING if php_running else ServiceStatus.STOPPED
        if new_php_status != self.php_status:
            self.php_status = new_php_status
            if self.status_callback:
                self.status_callback('php', self.php_status)
        if not silent:
            self.log('Status refresh completed', 'INFO')
            return None


