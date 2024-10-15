import tkinter as tk
from tkinter import messagebox



# Create the main window
root = tk.Tk()
root.title("Sample Tkinter App")

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save As...")
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Device Configuration")
help_menu.add_command(label="Using the autotuner")
help_menu.add_command(label="Saving recordings")
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Run the application
root.mainloop()