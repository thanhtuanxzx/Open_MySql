'''
App Bar - Top application bar with title and controls
'''
import webbrowser
from pathlib import Path
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Optional, Callable
from ui.style_manager import StyleManager

class AppBar(ttk.Frame):
    '''Application top bar with title and controls'''
    
    def __init__(self, parent, title, style_manager, on_setup = None, on_theme_toggle = None, on_about = None, logo_path = None, **kwargs):
        '''
Initialize AppBar

Args:
    parent: Parent widget
    title: Application title
    style_manager: StyleManager instance
    on_setup: Callback for setup button
    on_theme_toggle: Callback for theme toggle
    logo_path: Path to logo image file
'''
        super().__init__(parent, **kwargs)
        self.title = title
        self.style_manager = style_manager
        self.on_setup = on_setup
        self.on_theme_toggle = on_theme_toggle
        self.on_about = on_about
        self.logo_path = logo_path
        self.logo_image = None
        self._create_widgets()

    
    def _create_widgets(self):
        '''Create app bar widgets'''
        if self.logo_path and self.logo_path.exists():
            
            try:
                img = Image.open(self.logo_path)
                img.thumbnail((60, 40), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)
                logo_label = ttk.Label(self, image = self.logo_image)
                logo_label.pack(side = LEFT, padx = (0, 12))
            except Exception:
                pass

        title_label = ttk.Label(self, text = self.title, font = ('Segoe UI', 18, 'bold'))
        title_label.pack(side = LEFT, padx = (0, 20))
        version_label = ttk.Label(self, text = 'v2.0', font = ('Segoe UI', 10), foreground = '#6c757d')
        version_label.pack(side = LEFT, padx = (0, 20))
        author_label = ttk.Label(self, text = 'by thanhtuanxzx', font = ('Segoe UI', 9), foreground = '#6c757d', cursor = 'hand2')
        author_label.pack(side = LEFT)
        author_label.bind('<Button-1>', (lambda e: self._open_github()))
        ttk.Frame(self).pack(side = LEFT, fill = BOTH, expand = True)
        if self.on_setup:
            setup_btn = ttk.Button(self, text = '⚙️ Thiết lập ban đầu', command = self.on_setup, bootstyle = SECONDARY, padding = (12, 8))
            setup_btn.pack(side = RIGHT, padx = (8, 0))
        if self.on_theme_toggle:
            theme_btn = ttk.Button(self, text = '🌓', command = self.on_theme_toggle, bootstyle = OUTLINE, width = 3, padding = (8, 8))
            theme_btn.pack(side = RIGHT, padx = (8, 0))
        if self.on_about:
            about_btn = ttk.Button(self, text = 'ℹ️', command = self.on_about, bootstyle = OUTLINE, width = 3, padding = (8, 8))
            about_btn.pack(side = RIGHT, padx = (8, 0))
            return None

    
    def _open_github(self):
        '''Open GitHub profile'''
        webbrowser.open('https://github.com/thanhtuanxzx')


