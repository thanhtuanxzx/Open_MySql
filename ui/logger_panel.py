'''
Logger Panel - Thread-safe logging panel with scrollable text area
'''
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext
import queue
import threading
from typing import Optional
from pathlib import Path

class LoggerPanel(ttk.Frame):
    '''Thread-safe logging panel'''
    
    def __init__(self, parent, log_queue, show_header = True, **kwargs):
        '''
Initialize LoggerPanel

Args:
    parent: Parent widget
    log_queue: Queue for log messages (thread-safe)
    show_header: Whether to show header with title (default: True)
'''
        super().__init__(parent, **kwargs)
        self.log_queue = log_queue
        self.text_widget = None
        self.is_running = True
        self._create_widgets(show_header = show_header)
        self._start_queue_processor()

    
    def _create_widgets(self, show_header = True):
        '''Create logger panel widgets'''
        if show_header:
            header = ttk.Frame(self)
            header.pack(fill = X, pady = (0, 12))
            title = ttk.Label(header, text = 'Log & Trạng thái', font = ('Segoe UI', 12, 'bold'))
            title.pack(side = LEFT)
            refresh_btn = ttk.Button(header, text = '🔄 Làm mới trạng thái', bootstyle = PRIMARY, padding = (10, 6))
            refresh_btn.pack(side = RIGHT)
            self.refresh_btn = refresh_btn
        else:
            header = ttk.Frame(self)
            header.pack(fill = X, pady = (0, 8))
            refresh_btn = ttk.Button(header, text = '🔄 Làm mới', bootstyle = OUTLINE, padding = (8, 4))
            refresh_btn.pack(side = RIGHT)
            self.refresh_btn = refresh_btn
        text_frame = ttk.Frame(self)
        text_frame.pack(fill = BOTH, expand = True)
        self.text_widget = scrolledtext.ScrolledText(text_frame, wrap = 'word', font = ('Consolas', 9), state = 'disabled', height = 15)
        self.text_widget.pack(fill = BOTH, expand = True)

    
    def _start_queue_processor(self):
        '''Start processing log queue'''
        
        def process_queue():
            while self.is_running:
                
                try:
                    message = self.log_queue.get(timeout = 0.1)
                    self._append_log(message)
                    self.log_queue.task_done()
                except queue.Empty:
                    pass

                except Exception as e:
                    print(f'''Error processing log queue: {e}''')

        thread = threading.Thread(target = process_queue, daemon = True)
        thread.start()

    
    def _append_log(self, message):
        '''Append log message to text widget (must be called from main thread)'''
        if self.text_widget:
            self.text_widget.config(state = 'normal')
            self.text_widget.insert('end', message + '\n')
            self.text_widget.see('end')
            self.text_widget.config(state = 'disabled')
            return None

    
    def clear(self):
        '''Clear log panel'''
        if self.text_widget:
            self.text_widget.config(state = 'normal')
            self.text_widget.delete('1.0', 'end')
            self.text_widget.config(state = 'disabled')
            return None

    
    def destroy(self):
        '''Cleanup on destroy'''
        self.is_running = False
        super().destroy()


