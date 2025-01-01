import tkinter as tk
from tkinter import ttk

class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.status_label = ttk.Label(self, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X)
    
    def set_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)