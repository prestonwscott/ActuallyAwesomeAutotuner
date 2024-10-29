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
        file_menu.add_command(label="Save As...", command=utils.save_audio)
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
        content = Content(left_frame)
        content.pack(padx=60, pady=60)

        # Right frame
        right_frame = tk.Frame(main_frame, bg='light green')

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
        self.dynamic_canvas = get_dynamic_canvas() #Canvas that will be updated every 100 ms
        self.meters = get_meters()
        self.update_DBmeter()

    # The dynamic updates must be initialized
    def update_DBmeter(self):
        if self.meters:
            for m in self.meters:
                self.dynamic_canvas.delete(m)
            self.meters = []
        max_height = 533
        decibels_L,decibels_R = get_decibels()
        height_L = (max_height * (abs(decibels_L)/60))
        height_R = (max_height * (abs(decibels_R)/60))

        left_meter = self.dynamic_canvas.create_rectangle(10, height_L, 34, max_height, fill='light green', outline='')
        right_meter = self.dynamic_canvas.create_rectangle(38, height_R, 62, max_height, fill='light green', outline='')
        self.meters.append(left_meter)
        self.meters.append(right_meter)
        self.root.after(100, self.update_DBmeter)
    
        pass


if __name__ == "__main__":
    # Initialize the window
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()