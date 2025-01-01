import tkinter as tk
from tkinter import ttk, messagebox

class CreateTableDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Create New Table")
        self.geometry("400x400")
        
        self.columns = []
        self.setup_ui()
    
    def setup_ui(self):
        # Table name
        ttk.Label(self, text="Table Name:").pack(padx=5, pady=5)
        self.table_name = ttk.Entry(self)
        self.table_name.pack(fill=tk.X, padx=5)
        
        # Columns frame
        self.columns_frame = ttk.LabelFrame(self, text="Columns")
        self.columns_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add initial column
        self.add_column()
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Column", 
                  command=self.add_column).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create", 
                  command=self.create_table).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.destroy).pack(side=tk.RIGHT)
    
    def add_column(self):
        frame = ttk.Frame(self.columns_frame)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        name = ttk.Entry(frame)
        name.pack(side=tk.LEFT, padx=2)
        
        type_var = tk.StringVar(value="TEXT")
        type_combo = ttk.Combobox(frame, textvariable=type_var, 
                                values=["TEXT", "INTEGER", "REAL", "BLOB"])
        type_combo.pack(side=tk.LEFT, padx=2)
        
        self.columns.append((name, type_var))
    
    def create_table(self):
        table_name = self.table_name.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Please enter a table name")
            return
        
        columns = []
        for name_entry, type_var in self.columns:
            name = name_entry.get().strip()
            if name:
                columns.append((name, type_var.get()))
        
        if not columns:
            messagebox.showerror("Error", "Please add at least one column")
            return
        
        try:
            self.parent.db_manager.create_table(table_name, columns)
            self.parent.refresh_tables_list()
            self.parent.status_bar.set_status(f"Created table: {table_name}")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create table: {e}")