import tkinter as tk
from tkinter import *
from tkinter import ttk
from src import *

class MainApp:
    def __init__(self, root):
        self.root = root
        root.title("Autotuner")
        # Set the window geometry
        root.resizable(width=True, height=True)

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

        # Main frame to hold everything
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame
        left_frame = tk.Frame(main_frame)
        #left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content = Content(left_frame)
        content.pack(padx=60, pady=60)

        # Right frame
        right_frame = tk.Frame(main_frame, bg='light green')
        #right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create the notebook in the right frame
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create the effects and devices tabs
        effects_tab = ttk.Frame(notebook)
        notebook.add(effects_tab, text="Effects")

        devices_tab = ttk.Frame(notebook)
        notebook.add(devices_tab, text="Devices")

        # Add example content to the tabs to make them visible
        tk.Label(effects_tab, text="This is the Effects tab").pack()
        tk.Label(devices_tab, text="This is the Devices tab").pack()


        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    # Initialize the window
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
