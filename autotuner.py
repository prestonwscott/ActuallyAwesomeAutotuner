import tkinter as tk
from tkinter import *
from tkinter import ttk
from src import *

class MainApp:
    def __init__(self, root):
        self.root = root
        root.title("Autotuner")
        root.resizable(width=True, height=True)

        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save As...", command=utils.save_audio)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Device Configuration", command=self.open_device_config)
        help_menu.add_command(label="Using the autotuner")
        help_menu.add_command(label="Saving recordings")
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menu_bar)

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame
        left_frame = tk.Frame(main_frame, bg=window_color)
        content = Content(left_frame)
        content.pack(padx=60, pady=60)
        
        # Right frame
        style = ttk.Style()
        right_frame = tk.Frame(main_frame, bg=window_color)
        style.configure("TNotebook", background=window_color)
        style.configure("TNotebook.Tab", background=window_color, padding=[10, 5])
        self.notebook = ttk.Notebook(right_frame, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.effects_tab = tk.Frame(self.notebook)
        self.notebook.add(self.effects_tab, text="Effects")
        effects = Effect(self.effects_tab)
        effects.pack()

        self.devices_tab = tk.Frame(self.notebook, bg=window_color)
        self.notebook.add(self.devices_tab, text="Devices")
        devices = Devices(self.devices_tab)
        devices.pack()

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
        
    def open_device_config(self):
        self.notebook.select(self.devices_tab)
        print("Device Configuration Selected")

if __name__ == "__main__":
    # Initialize the window
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()