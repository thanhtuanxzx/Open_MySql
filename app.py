'''
Open MySQL - Portable MySQL Manager
Made by thanhtuanxzx - https://github.com/thanhtuanxzx
Modern UI with ttkbootstrap
'''
import sys
import os
from pathlib import Path
import threading
import webbrowser
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
sys.path.insert(0, str(Path(__file__).parent))
from services.service_controller import ServiceController, ServiceStatus
from services.config_manager import ConfigManager
from ui.style_manager import StyleManager
from ui.components import StatusCard, ActionButton
from ui.app_bar import AppBar
from ui.logger_panel import LoggerPanel

class MySQLManagerApp:
    '''Main application class'''
    
    def __init__(self):
        '''Initialize application'''
        if getattr(sys, 'frozen', False):
            self.base_dir = Path(sys.executable).parent.resolve()
            if hasattr(sys, '_MEIPASS'):
                config_dir = self.base_dir / 'config'
            else:
                config_dir = self.base_dir / 'config'
        else:
            self.base_dir = Path(__file__).parent.resolve()
            config_dir = self.base_dir / 'config'
        self.config = ConfigManager(config_dir)
        if not (self.base_dir / 'config').exists() and config_dir.exists():
            
            try:
                import shutil
                if hasattr(sys, '_MEIPASS'):
                    source_config = Path(sys._MEIPASS) / 'config'
                    if source_config.exists():
                        shutil.copytree(source_config, self.base_dir / 'config', dirs_exist_ok = True)
            except:
                pass

        theme = 'flatly' if self.config.get('theme', 'light') == 'light' else 'darkly'
        self.root = ttk.Window(themename = theme)
        self.root.title('Open MySQL v2.0 - by thanhtuanxzx')
        self.root.geometry('1100x700')
        self.root.minsize(1100, 700)
        ico_path = self.base_dir / 'logo.ico'
        logo_path = self.base_dir / 'logo.jpg'
        self.window_icon = None
        if ico_path.exists():
            
            try:
                self.root.iconbitmap(str(ico_path))
            except Exception:
                pass

        icon_img = None
        if ico_path.exists():
            
            try:
                icon_img = Image.open(ico_path)
            except Exception:
                pass

        if icon_img is not None and logo_path.exists():
            
            try:
                icon_img = Image.open(logo_path)
            except Exception:
                pass

        if icon_img:
            
            try:
                icon_img = icon_img.resize((128, 128), Image.Resampling.LANCZOS)
                self.window_icon = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(True, self.window_icon)
            except Exception:
                pass

        self.style_manager = StyleManager(self.root, theme)
        self.service_controller = ServiceController(self.base_dir, status_callback = self.on_status_update)
        self._create_ui()
        self.root.after(100, (lambda : self.service_controller.refresh_status()))
        self._start_status_refresh()
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)

    
    def _create_ui(self):
        '''Create user interface'''
        self.root.columnconfigure(0, weight = 1)
        self.root.rowconfigure(1, weight = 1)
        logo_path = self.base_dir / 'logo.jpg'
        self.app_bar = AppBar(self.root, title = 'Open MySQL', style_manager = self.style_manager, on_setup = self.on_setup_clicked, on_theme_toggle = self.toggle_theme, on_about = self.show_about, logo_path = logo_path)
        self.app_bar.pack(fill = X, padx = 16, pady = (16, 0))
        main_container = ttk.Frame(self.root)
        main_container.pack(fill = BOTH, expand = True, padx = 16, pady = 16)
        main_container.columnconfigure(0, weight = 1)
        main_container.rowconfigure(0, weight = 1)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill = BOTH, expand = True)
        self.functions_tab = ttk.Frame(self.notebook, padding = 16)
        self.notebook.add(self.functions_tab, text = 'Chức năng chính')
        self._create_functions_tab()
        self.status_tab = ttk.Frame(self.notebook, padding = 16)
        self.notebook.add(self.status_tab, text = 'Trạng thái')
        self._create_status_tab()
        self.settings_tab = ttk.Frame(self.notebook, padding = 16)
        self.notebook.add(self.settings_tab, text = 'Thiết lập')
        self._create_settings_tab()
        self.logs_tab = ttk.Frame(self.notebook, padding = 16)
        self.notebook.add(self.logs_tab, text = 'Log & Trạng thái')
        self._create_logs_tab()
        self.notebook.select(0)

    
    def _create_status_tab(self):
        '''Create status tab with service cards'''
        self.status_tab.columnconfigure((0, 1), weight = 1, uniform = 'cols')
        self.status_tab.rowconfigure(1, weight = 1)
        self.mysql_card = StatusCard(self.status_tab, title = 'MySQL Server', style_manager = self.style_manager, on_start = (lambda : self.service_controller.start_mysql()), on_stop = (lambda : self.service_controller.stop_mysql()), status = ServiceStatus.STOPPED)
        self.mysql_card.grid(row = 0, column = 0, sticky = (W, E, N, S), padx = (0, 8), pady = (0, 12))
        self.php_card = StatusCard(self.status_tab, title = 'PHP Web Server', style_manager = self.style_manager, on_start = (lambda : self.service_controller.start_php()), on_stop = (lambda : self.service_controller.stop_php()), status = ServiceStatus.STOPPED)
        self.php_card.grid(row = 0, column = 1, sticky = (W, E, N, S), padx = (8, 0), pady = (0, 12))

    
    def _create_functions_tab(self):
        '''Create main functions tab with log panel'''
        self.functions_tab.columnconfigure(0, weight = 1)
        self.functions_tab.rowconfigure(1, weight = 1)
        top_frame = ttk.Frame(self.functions_tab)
        top_frame.pack(fill = X, pady = (0, 16))
        top_frame.columnconfigure(0, weight = 1)
        title = ttk.Label(top_frame, text = 'Chức năng chính', font = ('Segoe UI', 16, 'bold'))
        title.pack(pady = (0, 20))
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(fill = X, pady = 8)
        btn_frame.columnconfigure((0, 1), weight = 1)
        start_pma_btn = ActionButton(btn_frame, text = '🚀 Khởi động phpMyAdmin', command = self.start_phpmyadmin, bootstyle = SUCCESS, size = 'large')
        start_pma_btn.grid(row = 0, column = 0, sticky = (W, E), padx = (0, 8))
        start_mysql_btn = ActionButton(btn_frame, text = '🗄️ Khởi động MySQL Server', command = (lambda : self.service_controller.start_mysql()), bootstyle = INFO, size = 'large')
        start_mysql_btn.grid(row = 0, column = 1, sticky = (W, E), padx = (8, 0))
        stop_all_btn = ActionButton(top_frame, text = '⏹ Dừng tất cả', command = self.stop_all, bootstyle = DANGER, size = 'large')
        stop_all_btn.pack(fill = X, pady = (12, 0))
        separator = ttk.Separator(self.functions_tab, orient = HORIZONTAL)
        separator.pack(fill = X, pady = (16, 16))
        log_frame = ttk.LabelFrame(self.functions_tab, text = 'Log hoạt động', padding = 12)
        log_frame.pack(fill = BOTH, expand = True)
        self.functions_logger = LoggerPanel(log_frame, self.service_controller.log_queue, show_header = False)
        self.functions_logger.pack(fill = BOTH, expand = True)
        self.functions_logger.refresh_btn.config(command = self.refresh_status)

    
    def _create_settings_tab(self):
        '''Create settings tab with improved design and horizontal layout'''
        canvas = ttk.Canvas(self.settings_tab)
        scrollbar = ttk.Scrollbar(self.settings_tab, orient = 'vertical', command = canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        canvas_window_id = canvas.create_window((0, 0), window = scrollable_frame, anchor = 'nw')
        
        def update_scroll_region(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window_id, width = canvas_width)
            canvas.configure(scrollregion = canvas.bbox('all'))

        canvas.bind('<Configure>', update_scroll_region)
        scrollable_frame.bind('<Configure>', (lambda e: canvas.configure(scrollregion = canvas.bbox('all'))))
        canvas.configure(yscrollcommand = scrollbar.set)
        canvas.pack(side = 'left', fill = 'both', expand = True)
        scrollbar.pack(side = 'right', fill = 'y')
        content = ttk.Frame(scrollable_frame, padding = 20)
        content.grid(row = 0, column = 0, sticky = (N, S, W, E))
        content.columnconfigure(0, weight = 1)
        content.columnconfigure(1, minsize = 900)
        content.columnconfigure(2, weight = 1)
        scrollable_frame.columnconfigure(0, weight = 1)
        setup_card = ttk.LabelFrame(content, text = '⚙️ Thiết lập ban đầu', padding = 20)
        setup_card.grid(row = 0, column = 1, sticky = (W, E), pady = (0, 16))
        setup_card.columnconfigure(0, weight = 1)
        setup_desc_frame = ttk.Frame(setup_card)
        setup_desc_frame.pack(fill = X, pady = (0, 16))
        setup_desc_frame.columnconfigure(0, weight = 1)
        setup_desc = ttk.Label(setup_desc_frame, text = 'Tự động cấu hình MySQL và phpMyAdmin cho lần đầu sử dụng. Tạo my.ini, config.inc.php và thiết lập các thông số cần thiết.', font = ('Segoe UI', 9), foreground = '#6c757d', justify = LEFT, wraplength = 600)
        setup_desc.grid(row = 0, column = 0, sticky = W)
        setup_btn = ActionButton(setup_card, text = '🚀 Bắt đầu thiết lập', command = self.on_setup_clicked, bootstyle = WARNING, size = 'large')
        setup_btn.pack(fill = X)
        other_card = ttk.LabelFrame(content, text = '🔧 Các chức năng khác', padding = 20)
        other_card.grid(row = 1, column = 1, sticky = (W, E), pady = (0, 16))
        other_card.columnconfigure(0, weight = 1)
        other_card.columnconfigure(1, weight = 1)
        other_card.columnconfigure(2, weight = 1, minsize = 16)
        fix_login_container = ttk.Frame(other_card)
        fix_login_container.grid(row = 0, column = 0, sticky = (W, E), padx = (0, 8))
        fix_login_container.columnconfigure(0, weight = 1)
        fix_login_desc = ttk.Label(fix_login_container, text = 'Sửa các vấn đề đăng nhập vào phpMyAdmin', font = ('Segoe UI', 8), foreground = '#6c757d')
        fix_login_desc.pack(anchor = W, pady = (0, 8))
        fix_login_btn = ttk.Button(fix_login_container, text = '🔐 Sửa lỗi đăng nhập', bootstyle = WARNING, command = self.fix_login, padding = (12, 10))
        fix_login_btn.pack(fill = X)
        separator = ttk.Separator(other_card, orient = VERTICAL)
        separator.grid(row = 0, column = 1, sticky = (N, S), padx = 16)
        update_paths_container = ttk.Frame(other_card)
        update_paths_container.grid(row = 0, column = 2, sticky = (W, E), padx = (8, 0))
        update_paths_container.columnconfigure(0, weight = 1)
        update_paths_desc = ttk.Label(update_paths_container, text = 'Cập nhật đường dẫn MySQL trong file my.ini', font = ('Segoe UI', 8), foreground = '#6c757d')
        update_paths_desc.pack(anchor = W, pady = (0, 8))
        update_paths_btn = ttk.Button(update_paths_container, text = '📁 Cập nhật đường dẫn', bootstyle = INFO, command = self.update_paths, padding = (12, 10))
        update_paths_btn.pack(fill = X)
        ports_card = ttk.LabelFrame(content, text = '🔌 Cấu hình Ports', padding = 20)
        ports_card.grid(row = 2, column = 1, sticky = (W, E))
        ports_card.columnconfigure(0, weight = 1)
        ports_card.columnconfigure(1, weight = 1)
        ports_desc = ttk.Label(ports_card, text = 'Thay đổi ports cho MySQL Server và PHP Web Server. Đảm bảo ports không bị xung đột với các ứng dụng khác.', font = ('Segoe UI', 9), foreground = '#6c757d', justify = LEFT, wraplength = 600)
        ports_desc.grid(row = 0, column = 0, columnspan = 2, sticky = W, pady = (0, 20))
        mysql_port_container = ttk.Frame(ports_card)
        mysql_port_container.grid(row = 1, column = 0, sticky = (W, E), padx = (0, 12))
        mysql_port_container.columnconfigure(0, weight = 1)
        mysql_port_label_frame = ttk.Frame(mysql_port_container)
        mysql_port_label_frame.pack(fill = X, pady = (0, 8))
        ttk.Label(mysql_port_label_frame, text = 'MySQL Server Port', font = ('Segoe UI', 10, 'bold')).pack(side = LEFT)
        mysql_port_help = ttk.Label(mysql_port_label_frame, text = '(Mặc định: 3306)', font = ('Segoe UI', 8), foreground = '#6c757d')
        mysql_port_help.pack(side = LEFT, padx = (8, 0))
        self.mysql_port_var = ttk.StringVar(value = str(self.config.get('mysql.port', 3306)))
        mysql_port_entry = ttk.Entry(mysql_port_container, textvariable = self.mysql_port_var, font = ('Consolas', 10))
        mysql_port_entry.pack(fill = X)
        php_port_container = ttk.Frame(ports_card)
        php_port_container.grid(row = 1, column = 1, sticky = (W, E), padx = (12, 0))
        php_port_container.columnconfigure(0, weight = 1)
        php_port_label_frame = ttk.Frame(php_port_container)
        php_port_label_frame.pack(fill = X, pady = (0, 8))
        ttk.Label(php_port_label_frame, text = 'PHP Web Server Port', font = ('Segoe UI', 10, 'bold')).pack(side = LEFT)
        php_port_help = ttk.Label(php_port_label_frame, text = '(Mặc định: 8080)', font = ('Segoe UI', 8), foreground = '#6c757d')
        php_port_help.pack(side = LEFT, padx = (8, 0))
        self.php_port_var = ttk.StringVar(value = str(self.config.get('php.port', 8080)))
        php_port_entry = ttk.Entry(php_port_container, textvariable = self.php_port_var, font = ('Consolas', 10))
        php_port_entry.pack(fill = X)
        save_ports_btn = ttk.Button(ports_card, text = '💾 Lưu cấu hình Ports', bootstyle = PRIMARY, command = self.save_ports, padding = (12, 10))
        save_ports_btn.grid(row = 2, column = 0, columnspan = 2, sticky = (W, E), pady = (20, 0))

    
    def _create_logs_tab(self):
        '''Create logs tab'''
        self.logger_panel = LoggerPanel(self.logs_tab, self.service_controller.log_queue)
        self.logger_panel.pack(fill = BOTH, expand = True)
        self.logger_panel.refresh_btn.config(command = self.refresh_status)

    
    def _start_status_refresh(self):
        '''Start periodic status refresh with optimized frequency'''
        self._refresh_active = True
        self._refresh_interval = 8000
        
        def refresh():
            if not self._refresh_active:
                return None
            mysql_status = self.service_controller.mysql_status
            php_status = self.service_controller.php_status
            if not (not (mysql_status == ServiceStatus.RUNNING) and not (php_status == ServiceStatus.RUNNING) and not (mysql_status == ServiceStatus.STARTING) and not (php_status == ServiceStatus.STARTING) and not (mysql_status == ServiceStatus.STOPPING)) or php_status == ServiceStatus.STOPPING:
                self.service_controller.refresh_status(silent = True)
                self.root.after(self._refresh_interval, refresh)
                return None
            self.service_controller.refresh_status(silent = True)
            self.root.after(15000, refresh)

        self.root.after(1000, refresh)

    
    def on_status_update(self, service, status):
        '''Handle status update from service controller'''
        
        def update_ui():
            if service == 'mysql':
                self.mysql_card.update_status(status)
                return None
            if service == 'php':
                self.php_card.update_status(status)
                if status == ServiceStatus.RUNNING:
                    threading.Timer(1.0, (lambda : webbrowser.open(f'''http://localhost:{self.service_controller.php_port}/'''))).start()
                    return None
                return None

        self.root.after(0, update_ui)

    
    def start_phpmyadmin(self):
        '''Start phpMyAdmin'''
        self.service_controller.log('Starting phpMyAdmin...', 'INFO')
        self.service_controller.start_phpmyadmin()
        
        def refresh_after_start():
            import time
            time.sleep(2)
            self.service_controller.refresh_status(silent = True)

        threading.Thread(target = refresh_after_start, daemon = True).start()
        
        def open_browser():
            threading.Timer(3.0, (lambda : webbrowser.open(f'''http://localhost:{self.service_controller.php_port}'''))).start()

        threading.Thread(target = open_browser, daemon = True).start()

    
    def stop_all(self):
        '''Stop all services'''
        self.service_controller.stop_all()
        self.service_controller.refresh_status(silent = True)

    
    def toggle_theme(self):
        '''Toggle between light and dark theme'''
        current_theme = self.config.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.config.set('theme', new_theme)
        self.config.save()
        theme_name = 'flatly' if new_theme == 'light' else 'darkly'
        self.style_manager.set_theme(theme_name)
        self.root.style.theme_use(theme_name)
        if hasattr(self, 'mysql_card'):
            self.mysql_card.update_status(self.mysql_card.status)
        if hasattr(self, 'php_card'):
            self.php_card.update_status(self.php_card.status)
            return None

    
    def on_setup_clicked(self):
        '''Handle setup button click'''
        self.service_controller.log('Starting initial setup...', 'INFO')
        self.service_controller.update_my_ini()
        self.service_controller.log('Updated my.ini', 'SUCCESS')
        if not self.service_controller.config_file.exists():
            self.service_controller.create_phpmyadmin_config()
            self.service_controller.log('Created phpMyAdmin config', 'SUCCESS')
        self.service_controller.log('Setup completed!', 'SUCCESS')

    
    def fix_login(self):
        '''Fix phpMyAdmin login issue'''
        self.service_controller.create_phpmyadmin_config()
        self.service_controller.log('Fixed phpMyAdmin login configuration', 'SUCCESS')

    
    def update_paths(self):
        '''Update paths in configuration'''
        self.service_controller.update_my_ini()
        self.service_controller.log('Updated paths in my.ini', 'SUCCESS')

    
    def select_php_folder(self):
        '''Select PHP folder'''
        folder = filedialog.askdirectory(title = 'Chọn thư mục PHP')
        if folder:
            php_exe = Path(folder) / 'php.exe'
            if php_exe.exists():
                import shutil
                
                try:
                    if self.service_controller.php_dir.exists():
                        shutil.rmtree(self.service_controller.php_dir)
                    shutil.copytree(folder, self.service_controller.php_dir)
                    self.service_controller.log(f'''Copied PHP to {self.service_controller.php_dir}''', 'SUCCESS')
                    return None
                except Exception as e:
                    self.service_controller.log(f'''Failed to copy PHP: {e}''', 'ERROR')
                    return None

                return None

    
    def save_ports(self):
        '''Save port configuration'''
        
        try:
            mysql_port = int(self.mysql_port_var.get())
            php_port = int(self.php_port_var.get())
            self.config.set('mysql.port', mysql_port)
            self.config.set('php.port', php_port)
            self.config.save()
            self.service_controller.mysql_port = mysql_port
            self.service_controller.php_port = php_port
            self.service_controller.log(f'''Saved ports: MySQL={mysql_port}, PHP={php_port}''', 'SUCCESS')
        except ValueError:
            self.service_controller.log('Invalid port number', 'ERROR')
            return None


    
    def refresh_status(self):
        '''Refresh service statuses'''
        self.service_controller.refresh_status()

    
    def show_about(self):
        '''Show about dialog'''
        from tkinter import messagebox
        messagebox.showinfo('Về Open MySQL', 'Open MySQL v2.0\n\nPortable MySQL Manager với giao diện hiện đại\n\nMade by: thanhtuanxzx\nGitHub: https://github.com/thanhtuanxzx\n\n© 2025 thanhtuanxzx')

    
    def on_close(self):
        '''Handle window close'''
        from tkinter import messagebox
        import time
        self._refresh_active = False
        mysql_status = self.service_controller.mysql_status
        php_status = self.service_controller.php_status
        if (mysql_status == ServiceStatus.RUNNING or php_status == ServiceStatus.RUNNING) and messagebox.askokcancel('Thoát', 'Các services đang chạy. Bạn có muốn dừng tất cả và thoát không?'):
            self.stop_all()
            time.sleep(1)
        self.root.quit()
        self.root.destroy()

    
    def run(self):
        '''Run application'''
        self.root.mainloop()



def main():
    '''Main entry point'''
    app = MySQLManagerApp()
    app.run()

if __name__ == '__main__':
    main()
