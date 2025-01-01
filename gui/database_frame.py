import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class DatabaseFrame(ttk.LabelFrame):
    def __init__(self, parent, title, db_manager):
        super().__init__(parent, text=title, padding=10)
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        # Table list
        self.tables_frame = ttk.Frame(self)
        self.tables_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tables_list = tk.Listbox(self.tables_frame, exportselection=0)
        self.tables_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tables_list.bind('<<ListboxSelect>>', self.on_table_select)
        
        # Scrollbar for tables list
        scrollbar = ttk.Scrollbar(self.tables_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tables_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tables_list.yview)
        
        # Buttons
        self.create_buttons()
        
        # Data view
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def create_buttons(self):
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Open Database", 
                  command=self.open_database).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Create Table", 
                  command=self.create_table).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Add Data", 
                  command=self.add_data).pack(side=tk.LEFT, padx=2)
        
    def open_database(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")])
        if file_path:
            if self.db_manager.connect(file_path):
                self.refresh_tables_list()
                
    def refresh_tables_list(self):
        self.tables_list.delete(0, tk.END)
        for table in self.db_manager.get_tables():
            self.tables_list.insert(tk.END, table)
            
    def on_table_select(self, event):
        selection = self.tables_list.curselection()
        if selection:
            table_name = self.tables_list.get(selection[0])
            self.show_table_data(table_name)
            
    def show_table_data(self, table_name):
        # Clear existing columns
        self.tree.delete(*self.tree.get_children())
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        
        # Set new columns
        columns = self.db_manager.get_table_columns(table_name)
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            
        # Add data
        for row in self.db_manager.get_table_data(table_name):
            self.tree.insert("", tk.END, values=row)