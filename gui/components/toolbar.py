import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..dialogs.create_table_dialog import CreateTableDialog

class Toolbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        # Database operations
        ttk.Button(self, text="Open Database", 
                  command=self.open_database).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="Create Table", 
                  command=self.create_table).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="Refresh", 
                  command=self.parent.refresh_tables_list).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # Data operations
        ttk.Button(self, text="Add Data", 
                  command=self.add_data).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="Edit Data", 
                  command=self.edit_data).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text="Delete Data", 
                  command=self.delete_data).pack(side=tk.LEFT, padx=2)
    
    def open_database(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")])
        if file_path:
            if self.parent.db_manager.connect(file_path):
                self.parent.refresh_tables_list()
                self.parent.status_bar.set_status(f"Connected to: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to open database")
    
    def create_table(self):
        dialog = CreateTableDialog(self.parent)
        self.wait_window(dialog)
        self.parent.refresh_tables_list()
    
    def add_data(self):
        selection = self.parent.tables_list.curselection()
        if selection:
            table_name = self.parent.tables_list.get(selection[0])
            from ..dialogs.add_data_dialog import AddDataDialog
            dialog = AddDataDialog(self.parent, table_name)
            self.wait_window(dialog)
            self.parent.load_table_data(table_name)
    
    def edit_data(self):
        selection = self.parent.tables_list.curselection()
        if selection:
            table_name = self.parent.tables_list.get(selection[0])
            from ..dialogs.edit_data_dialog import EditDataDialog
            dialog = EditDataDialog(self.parent, table_name)
            self.wait_window(dialog)
            self.parent.load_table_data(table_name)
    
    def delete_data(self):
        selection = self.parent.tables_list.curselection()
        if selection:
            table_name = self.parent.tables_list.get(selection[0])
            if messagebox.askyesno("Confirm Delete", 
                                 "Are you sure you want to delete the selected data?"):
                try:
                    # Get selected items from table view
                    selected_items = self.parent.table_view.get_selected_items()
                    if selected_items:
                        # Delete selected items
                        for item in selected_items:
                            self.parent.db_manager.delete_data(table_name, f"rowid = {item}")
                        self.parent.load_table_data(table_name)
                        self.parent.status_bar.set_status("Data deleted successfully")
                    else:
                        messagebox.showwarning("Warning", "No items selected")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete data: {e}")