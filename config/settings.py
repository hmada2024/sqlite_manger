from tkinter import ttk

def setup_theme(root):
    """Configure the application theme and styles"""
    style = ttk.Style()
    
    # Configure main theme
    style.configure(".", font=('Helvetica', 10))
    
    # Configure Treeview
    style.configure("Treeview", 
                   rowheight=25,
                   font=('Helvetica', 10))
    style.configure("Treeview.Heading", 
                   font=('Helvetica', 10, 'bold'))
    
    # Configure Buttons
    style.configure("Primary.TButton",
                   padding=5,
                   font=('Helvetica', 10))
    
    # Configure Frames
    style.configure("Card.TFrame",
                   background="#ffffff",
                   relief="raised",
                   borderwidth=1)
    
    return style