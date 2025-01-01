import tkinter as tk
from tkinter import ttk, messagebox

class EditDataDialog(tk.Toplevel):
    def __init__(self, parent, table_name):
        super().__init__(parent)
        self.parent = parent
        self.table_name = table_name
        self.title(f"Edit Data - {table_name}")
        self.geometry("400x300")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Get selected items from table view
        selected = self.parent.table_view.get_selected_items()
        if not selected:
            messagebox.showwarning("Warning", "No items selected")
            self.destroy()
            return
        
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
        
        ttk.Button(button_frame, text="Save", 
                  command=self.save_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.destroy).pack(side=tk.RIGHT)
    
    def save_changes(self):
        try:
            # Update each selected item
            selected = self.parent.table_view.get_selected_items()
            for item in selected:
                for col, entry in self.entries.items():
                    value = entry.get()
                    if value:
                        self.parent.db_manager.update_data(
                            self.table_name, col, value, f"rowid = {item}")
            
            self.parent.load_table_data(self.table_name)
            self.parent.status_bar.set_status("Data updated successfully")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update data: {e}")