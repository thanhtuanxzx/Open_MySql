'''
Config Manager - Manages application configuration in JSON format
'''
import json
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    '''Manages application configuration'''
    
    def __init__(self, config_dir, config_file = 'config.json'):
        '''
Initialize ConfigManager

Args:
    config_dir: Directory for config files
    config_file: Config file name
'''
        self.config_dir = Path(config_dir)
        
        try:
            self.config_dir.mkdir(exist_ok = True, parents = True)
        except:
            pass

        self.config_file = self.config_dir / config_file
        self.config = { }
        self.load_default()
        if self.config_file.exists():
            self.load()
            return None
        self.save()

    
    def load_default(self):
        '''Load default configuration'''
        self.config = {
            'mysql': {
                'port': 3306,
                'data_dir': 'data',
                'basedir': 'MySQL Server 9.5',
                'my_ini_path': 'MySQL Server 9.5/my.ini' },
            'php': {
                'port': 8080,
                'php_dir': 'php',
                'php_exe_path': 'php/php.exe' },
            'phpmyadmin': {
                'dir': 'phpMyAdmin-5.2.3-all-languages',
                'config_path': 'phpMyAdmin-5.2.3-all-languages/config.inc.php' },
            'theme': 'light',
            'last_php_path': '' }

    
    def load(self):
        '''Load configuration from file'''
        
        try:
            with open(self.config_file, 'r', encoding = 'utf-8') as f:
                loaded = json.load(f)
                self._deep_update(self.config, loaded)
            return True
        except Exception as e:
            print(f'''Error loading config: {e}''')
            return False


    
    def save(self):
        '''Save configuration to file'''
        
        try:
            with open(self.config_file, 'w', encoding = 'utf-8') as f:
                json.dump(self.config, f, indent = 2, ensure_ascii = False)
            return True
        except Exception as e:
            print(f'''Error saving config: {e}''')
            return False


    
    def get(self, key, default = None):
        """Get config value by key (supports dot notation: 'mysql.port')"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
                continue
            return default
        return value

    
    def set(self, key, value):
        """Set config value by key (supports dot notation: 'mysql.port')"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = { }
            config = config[k]
        config[keys[-1]] = value

    
    def _deep_update(self, base, update):
        '''Deep update dictionary'''
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
                continue
            base[key] = value


