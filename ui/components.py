'''
UI Components - Reusable UI components with ttkbootstrap
'''
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Optional, Callable
from pathlib import Path
from ui.style_manager import StyleManager
from services.service_controller import ServiceStatus

class StatusCard(ttk.Frame):
    '''Status card component with icon, status badge, and action buttons'''
    
    def __init__(self, parent, title, style_manager, on_start = None, on_stop = None, status = ServiceStatus.STOPPED, **kwargs):
        '''
Initialize StatusCard

Args:
    parent: Parent widget
    title: Card title
    style_manager: StyleManager instance
    on_start: Callback for start button
    on_stop: Callback for stop button
    status: Initial status
'''
        super().__init__(parent, style = 'Card.TFrame', padding = 16, **kwargs)
        self.title = title
        self.style_manager = style_manager
        self.on_start = on_start
        self.on_stop = on_stop
        self.status = status
        self._create_widgets()
        self.update_status(status)

    
    def _create_widgets(self):
        '''Create card widgets'''
        title_frame = ttk.Frame(self)
        title_frame.pack(fill = X, pady = (0, 12))
        self.icon_label = ttk.Label(title_frame, text = '●', font = ('Segoe UI', 16))
        self.icon_label.pack(side = LEFT, padx = (0, 8))
        title_label = ttk.Label(title_frame, text = self.title, font = ('Segoe UI', 13, 'bold'), style = 'Card.TLabel')
        title_label.pack(side = LEFT, fill = X, expand = True)
        self.status_label = ttk.Label(title_frame, text = 'Không chạy', style = 'StatusStopped.TLabel')
        self.status_label.pack(side = RIGHT)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill = X, pady = (12, 0))
        btn_frame.columnconfigure(0, weight = 1)
        btn_frame.columnconfigure(1, weight = 1)
        self.start_btn = ttk.Button(btn_frame, text = 'Khởi động', command = self.on_start, style = 'Success.TButton', bootstyle = SUCCESS)
        self.start_btn.grid(row = 0, column = 0, sticky = (W, E), padx = (0, 6))
        self.stop_btn = ttk.Button(btn_frame, text = 'Dừng', command = self.on_stop, style = 'Danger.TButton', bootstyle = DANGER)
        self.stop_btn.grid(row = 0, column = 1, sticky = (W, E), padx = (6, 0))

    
    def update_status(self, status):
        '''Update card status'''
        self.status = status
        if status == ServiceStatus.RUNNING:
            status_key = 'running'
            self.start_btn.config(state = DISABLED)
            self.stop_btn.config(state = NORMAL)
        elif status == ServiceStatus.STOPPED:
            status_key = 'stopped'
            self.start_btn.config(state = NORMAL)
            self.stop_btn.config(state = DISABLED)
        elif status == ServiceStatus.STARTING:
            status_key = 'starting'
            self.start_btn.config(state = DISABLED)
            self.stop_btn.config(state = DISABLED)
        elif status == ServiceStatus.STOPPING:
            status_key = 'stopping'
            self.start_btn.config(state = DISABLED)
            self.stop_btn.config(state = DISABLED)
        else:
            status_key = 'error'
            self.start_btn.config(state = NORMAL)
            self.stop_btn.config(state = DISABLED)
        style_name, colors = self.style_manager.get_status_style(status_key)
        self.status_label.config(text = colors['text'], style = style_name)
        if status == ServiceStatus.RUNNING:
            self.icon_label.config(text = '●', foreground = '#198754')
            return None
        if status == ServiceStatus.ERROR:
            self.icon_label.config(text = '●', foreground = '#dc3545')
            return None
        self.icon_label.config(text = '●', foreground = '#6c757d')



class ActionButton(ttk.Button):
    '''Large action button component'''
    
    def __init__(self, parent, text, command = None, bootstyle = PRIMARY, size = 'large', **kwargs):
        '''
Initialize ActionButton

Args:
    parent: Parent widget
    text: Button text
    command: Command callback
    bootstyle: Bootstrap style (PRIMARY, SUCCESS, DANGER, etc.)
    size: Button size (large, medium, small)
'''
        size_configs = {
            'large': {
                'padding': (20, 14),
                'font_size': 13 },
            'medium': {
                'padding': (16, 12),
                'font_size': 11 },
            'small': {
                'padding': (12, 10),
                'font_size': 10 } }
        config = size_configs.get(size, size_configs['medium'])
        style_name = f'''ActionButton{size.capitalize()}.TButton'''
        kwargs.pop('font', None)
        kwargs.pop('padding', None)
        super().__init__(parent, text = text, command = command, bootstyle = bootstyle, style = style_name, **kwargs)


