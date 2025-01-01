import tkinter as tk
from tkinter import ttk

class TableView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Create Treeview
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    def display_data(self, columns, data):
        # Clear existing data
        self.tree.delete(*self.tree.get_children())
        
        # Configure columns
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=100)
        
        # Add data
        for row in data:
            self.tree.insert("", tk.END, values=row)
    
    def sort_column(self, col):
        """Sort tree contents when a column header is clicked"""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        l.sort()
        
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, "", index)
    
    def get_selected_items(self):
        """Return the selected items"""
        return self.tree.selection()
    
    def clear(self):
        """Clear all data from the table"""
        self.tree.delete(*self.tree.get_children())