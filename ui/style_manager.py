'''
Style Manager - Manages ttkbootstrap themes and styles
'''
import ttkbootstrap as ttk
from typing import Optional, Dict, Any

class StyleManager:
    '''Manages application styles and themes'''
    COLORS = {
        'primary': '#0d6efd',
        'success': '#198754',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#0dcaf0',
        'secondary': '#6c757d',
        'dark': '#212529',
        'light': '#f8f9fa' }
    STATUS_COLORS_LIGHT = {
        'running': {
            'bg': '#d1e7dd',
            'fg': '#0f5132',
            'text': 'Đang chạy' },
        'stopped': {
            'bg': '#e9ecef',
            'fg': '#495057',
            'text': 'Không chạy' },
        'error': {
            'bg': '#f8d7da',
            'fg': '#842029',
            'text': 'Lỗi' },
        'starting': {
            'bg': '#fff3cd',
            'fg': '#664d03',
            'text': 'Đang khởi động...' },
        'stopping': {
            'bg': '#fff3cd',
            'fg': '#664d03',
            'text': 'Đang dừng...' } }
    STATUS_COLORS_DARK = {
        'running': {
            'bg': '#1e4d3a',
            'fg': '#86d4a8',
            'text': 'Đang chạy' },
        'stopped': {
            'bg': '#3d3d3d',
            'fg': '#b0b0b0',
            'text': 'Không chạy' },
        'error': {
            'bg': '#5a2a2a',
            'fg': '#ff8a8a',
            'text': 'Lỗi' },
        'starting': {
            'bg': '#5a4a2a',
            'fg': '#ffd98a',
            'text': 'Đang khởi động...' },
        'stopping': {
            'bg': '#5a4a2a',
            'fg': '#ffd98a',
            'text': 'Đang dừng...' } }
    
    @property
    def STATUS_COLORS(self):
        '''Get status colors based on current theme'''
        is_dark = self.theme == 'darkly'
        if is_dark:
            return self.STATUS_COLORS_DARK
        return self.STATUS_COLORS_LIGHT

    
    def __init__(self, root = None, theme = 'flatly'):
        '''
Initialize StyleManager

Args:
    root: Root window
    theme: Theme name (flatly for light, darkly for dark)
'''
        self.root = root
        self.theme = theme
        self.style = None
        if root:
            self.setup_style()
            return None

    
    def setup_style(self):
        '''Setup ttkbootstrap style'''
        if self.root:
            self.style = ttk.Style(self.theme)
            self._apply_custom_styles()
            return None

    
    def _apply_custom_styles(self):
        '''Apply custom styles to widgets'''
        if not self.style:
            return None
        is_dark = self.theme == 'darkly'
        self.style.configure('Primary.TButton', foreground = 'white', font = ('Segoe UI', 11, 'bold'))
        self.style.configure('Success.TButton', foreground = 'white', font = ('Segoe UI', 11, 'bold'))
        self.style.configure('Danger.TButton', foreground = 'white', font = ('Segoe UI', 11, 'bold'))
        self.style.configure('ActionButtonLarge.TButton', font = ('Segoe UI', 13, 'bold'))
        self.style.configure('ActionButtonMedium.TButton', font = ('Segoe UI', 11, 'bold'))
        self.style.configure('ActionButtonSmall.TButton', font = ('Segoe UI', 10, 'bold'))
        card_bg = '#2b2b2b' if is_dark else 'white'
        card_fg = '#e0e0e0' if is_dark else 'black'
        self.style.configure('Card.TFrame', background = card_bg, foreground = card_fg, relief = 'flat', borderwidth = 1)
        self.style.configure('Card.TLabel', background = card_bg, foreground = card_fg)
        status_colors = self.STATUS_COLORS
        self.style.configure('StatusRunning.TLabel', background = status_colors['running']['bg'], foreground = status_colors['running']['fg'], padding = (8, 4), font = ('Segoe UI', 9, 'bold'), relief = 'flat')
        self.style.configure('StatusStopped.TLabel', background = status_colors['stopped']['bg'], foreground = status_colors['stopped']['fg'], padding = (8, 4), font = ('Segoe UI', 9, 'bold'), relief = 'flat')
        self.style.configure('StatusError.TLabel', background = status_colors['error']['bg'], foreground = status_colors['error']['fg'], padding = (8, 4), font = ('Segoe UI', 9, 'bold'), relief = 'flat')
        self.style.configure('StatusStarting.TLabel', background = status_colors['starting']['bg'], foreground = status_colors['starting']['fg'], padding = (8, 4), font = ('Segoe UI', 9, 'bold'), relief = 'flat')
        self.style.configure('StatusStopping.TLabel', background = status_colors['stopping']['bg'], foreground = status_colors['stopping']['fg'], padding = (8, 4), font = ('Segoe UI', 9, 'bold'), relief = 'flat')

    
    def set_theme(self, theme):
        '''Change theme (flatly for light, darkly for dark)'''
        self.theme = theme
        if self.root:
            self.style.theme_use(theme)
            self._apply_custom_styles()
            return None

    
    def get_status_style(self, status):
        '''
Get status badge style

Args:
    status: Status name (running, stopped, error, starting, stopping)
    
Returns:
    Tuple of (style_name, color_dict)
'''
        status_lower = status.lower()
        if status_lower in self.STATUS_COLORS:
            style_name = f'''Status{status_lower.capitalize()}.TLabel'''
            colors = self.STATUS_COLORS[status_lower]
            return (style_name, colors)
        return ('StatusStopped.TLabel', self.STATUS_COLORS['stopped'])


