import tkinter as tk
from tkinter import ttk

# Initialize the window
root = tk.Tk()
root.title("Autotuner")
# Set the window gemetry (Size) and make it  not resizable
root.geometry("800x500")
root.resizable(False, False)
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


main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

# Configure the grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# Position left frame
left_frame = tk.Frame(main_frame, width=400, height=600, bg='light gray')
left_frame.grid(row=0, column=0, sticky="nsew")

# Position right frame
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew")


# Position notebook within right frame
notebook = ttk.Notebook(right_frame)
notebook.grid(row=0, column=0, sticky="nsew")

# Create the effects and devices tabs
effects_tab = tk.Frame(notebook)
effects_tab.pack(fill=tk.BOTH, expand=True)
notebook.add(effects_tab, text="Effects")

devices_tab = tk.Frame(notebook)
devices_tab.pack(fill=tk.BOTH, expand=True)
notebook.add(devices_tab, text="Devices")


# Run the application
root.mainloop()