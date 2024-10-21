import tkinter as tk

def darken_color(parent, color, factor):
    r, g, b = parent.winfo_rgb(color)
    r = int(r * factor) // 256
    g = int(g * factor) // 256
    b = int(b * factor) // 256
    return f'#{r:02x}{g:02x}{b:02x}'

def on_enter(parent, shapes, factor):
    for shape in shapes:
        current_color = parent.itemcget(shape, "fill")
        new_color = darken_color(parent, current_color, factor)
        parent.itemconfig(shape, fill=new_color)

def on_leave(parent, shapes, factor):
    for shape in shapes:
        current_color = parent.itemcget(shape, "fill")
        new_color = darken_color(parent, current_color, 1/factor)
        parent.itemconfig(shape, fill=new_color)

def create_rounded_rect(parent, width, height, color):
    radius = 30
    offset = 0

    shapes = []
    shapes.append(parent.create_oval(offset, offset, offset + radius, offset + radius, fill=color, outline=""))
    shapes.append(parent.create_oval(offset + width - radius, offset, offset + width, offset + radius, fill=color, outline=""))
    shapes.append(parent.create_oval(offset, offset + height - radius, offset + radius, offset + height, fill=color, outline=""))
    shapes.append(parent.create_oval(offset + width - radius, offset + height - radius, offset + width, offset + height, fill=color, outline=""))
    shapes.append(parent.create_rectangle(offset + radius / 2, offset, offset + width - radius / 2, offset + height, fill=color, outline=""))
    shapes.append(parent.create_rectangle(offset, offset + radius / 2, offset + width, offset + height - radius / 2, fill=color, outline=""))
    return shapes

def create_panel(parent, width, height, color):
    frame = tk.Frame(parent)
    canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0)
    create_rounded_rect(canvas, width, height, color)

    canvas.pack()
    frame.pack()
    return frame

def create_button(parent, width, height, color, icon_path, factor=0.7):
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    shapes = create_rounded_rect(canvas, width, height, color)
    icon_photo = tk.PhotoImage(file=icon_path)
    canvas.create_image(width / 2, height / 2, image=icon_photo)
    canvas.image = icon_photo

    canvas.bind("<Button-1>", lambda e: print("Button clicked!"))
    canvas.bind("<Enter>", lambda e: on_enter(canvas, shapes, factor))
    canvas.bind("<Leave>", lambda e: on_leave(canvas, shapes, factor))
    canvas.pack()
    return canvas

def create_dial(parent, size, label_txt, subtitle_txt, default, min, max):
    canvas = tk.Canvas(parent, width=size, height=size*(18/11))
    label = tk.Label(canvas, text=label_txt, font=("Default", 10, "bold"))
    subtitle_txt = subtitle_txt.replace("<n>", str(default))
    subtitle = tk.Label(canvas, text=subtitle_txt, font=("Default", 8))
    icon_photo = tk.PhotoImage(file="assets/dial.png")
    
    canvas.create_window(24, 10, window=label)
    canvas.create_window(24, 68, window=subtitle)
    canvas.create_image(24, 40, image=icon_photo)
    canvas.image = icon_photo
    
    return canvas

# Create main window
root = tk.Tk()

panel_tune = create_panel(root, 100, 208, "white")
#button_tune = create_button(panel_tune, 48, 48, "light grey", "assets/tunefork.png")
#button_tune.place(x=26, y=8)
dial_gain = create_dial(panel_tune, 44, "Gain", "<n> dB", 0.0, -36.0, 36.0)
dial_gain.place(x=30, y=64)

# Run the application
root.mainloop()

