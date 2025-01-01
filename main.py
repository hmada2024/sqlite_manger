import tkinter as tk
from tkinter import ttk
from gui.main_window import MainWindow
from config.settings import setup_theme

def main():
    root = tk.Tk()
    root.title("SQLite Database Manager")
    root.geometry("1200x800")
    
    # Setup theme and styles
    setup_theme(root)
    
    app = MainWindow(root)
    app.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main()