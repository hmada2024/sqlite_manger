import tkinter as tk
from tkinter import ttk, messagebox
from .components.toolbar import Toolbar
from .components.table_view import TableView
from .components.status_bar import StatusBar
from database.db_manager import DatabaseManager
from utils.file_operations import FileOperations

class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DatabaseManager()
        self.file_ops = FileOperations()
        
        self.setup_ui()
        self.create_bindings()
    
    def setup_ui(self):
        # Create toolbar
        self.toolbar = Toolbar(self)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Create main content area
        self.content = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create table list frame
        self.table_list_frame = ttk.LabelFrame(self.content, text="Tables")
        self.content.add(self.table_list_frame, weight=1)
        
        self.tables_list = tk.Listbox(self.table_list_frame, exportselection=0)
        self.tables_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create table view
        self.table_view = TableView(self.content)
        self.content.add(self.table_view, weight=3)
        
        # Create status bar
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_bindings(self):
        self.tables_list.bind('<<ListboxSelect>>', self.on_table_select)
    
    def on_table_select(self, event):
        selection = self.tables_list.curselection()
        if selection:
            table_name = self.tables_list.get(selection[0])
            self.load_table_data(table_name)
    
    def load_table_data(self, table_name):
        try:
            columns = self.db_manager.get_table_columns(table_name)
            data = self.db_manager.get_table_data(table_name)
            self.table_view.display_data(columns, data)
            self.status_bar.set_status(f"Loaded table: {table_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load table data: {e}")
    
    def refresh_tables_list(self):
        self.tables_list.delete(0, tk.END)
        tables = self.db_manager.get_tables()
        for table in tables:
            self.tables_list.insert(tk.END, table)
        self.status_bar.set_status("Tables list refreshed")