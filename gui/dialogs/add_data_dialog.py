import tkinter as tk
from tkinter import ttk, messagebox

class AddDataDialog(tk.Toplevel):
    def __init__(self, parent, table_name):
        super().__init__(parent)
        self.parent = parent
        self.table_name = table_name
        self.title(f"Add Data - {table_name}")
        self.geometry("400x300")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Get columns
        columns = self.parent.db_manager.get_table_columns(self.table_name)
        
        # Create entry fields for each column
        self.entries = {}
        for col in columns:
            frame = ttk.Frame(self)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=col).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[col] = entry
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add", 
                  command=self.add_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.destroy).pack(side=tk.RIGHT)
    
    def add_data(self):
        try:
            # Collect values from entries
            values = []
            for entry in self.entries.values():
                values.append(entry.get())
            
            # Insert data
            self.parent.db_manager.insert_data(self.table_name, [tuple(values)])
            
            self.parent.load_table_data(self.table_name)
            self.parent.status_bar.set_status("Data added successfully")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add data: {e}")