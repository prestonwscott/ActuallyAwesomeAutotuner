import tkinter as tk
from .utils import *

def darken_color(parent, color, factor):
    r, g, b = parent.winfo_rgb(color)
    r = int(r * factor) // 256
    g = int(g * factor) // 256
    b = int(b * factor) // 256
    return f'#{r:02x}{g:02x}{b:02x}'

def on_click(parent, id):
    print(id)
    if(id == "Microphone toggle"):
        record_audio(autotune)
        
    if(id == "Mute toggle"):
        mute_audio()

def on_enter(parent, shapes, factor):
    for shape in shapes:
        current_color = parent.itemcget(shape, "fill")
        new_color = darken_color(parent, current_color, factor)
        parent.itemconfig(shape, fill=new_color)

def on_leave(parent, shapes, factor):
    for shape in shapes:
        current_color = parent.itemcget(shape, "fill")
        if current_color == "#b3b3b3":
            parent.itemconfig(shape, fill="white")
        else:    
            new_color = darken_color(parent, current_color, 1/factor)
            parent.itemconfig(shape, fill=new_color)

def create_rounded_rect(parent, x, y, width, height, color):
    radius = 10
    points = [
            x + radius, y,                 # Top left corner
            x + width - radius, y,         # Top right corner
            x + width, y + radius,         # Top right arc
            x + width, y + height - radius, # Bottom right arc
            x + width - radius, y + height, # Bottom right corner
            x + radius, y + height,        # Bottom left corner
            x, y + height - radius,       # Bottom left arc
            x, y + radius                  # Top left arc
        ]

    shapes = []
    shapes.append(parent.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=90, fill=color, outline=""))
    shapes.append(parent.create_arc(x + width - 2 * radius, y, x + width, y + 2 * radius, start=0, extent=90, fill=color, outline=""))
    shapes.append(parent.create_arc(x + width - 2 * radius, y + height - 2 * radius, x + width, y + height, start=270, extent=90, fill=color, outline=""))
    shapes.append(parent.create_arc(x, y + height - 2 * radius, x + 2 * radius, y + height, start=180, extent=90, fill=color, outline=""))
    shapes.append(parent.create_rectangle(x + radius, y, x + width - radius, y + height, fill=color, outline=""))
    shapes.append(parent.create_rectangle(x, y + radius, x + width, y + height - radius, fill=color, outline=""))
    return shapes

def create_panel(parent, width, height, color, icon_path):
    frame = tk.Frame(parent)
    canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0)
    create_rounded_rect(canvas, 0, 0, width, height, color)
    if len(icon_path) != 0:
        icon_photo = tk.PhotoImage(file=icon_path)
        canvas.create_image(width / 2, height / 2, image=icon_photo)
        canvas.image = icon_photo

    canvas.pack()
    return frame

def create_button(parent, width, height, color, bgcolor, id, icon_path, factor=0.7):
    if len(bgcolor) == 0:
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    else:
        canvas = tk.Canvas(parent, width=width, height=height, bg=bgcolor, highlightthickness=0)
    shapes = create_rounded_rect(canvas, 0, 0, width, height, color)
    icon_photo = tk.PhotoImage(file=icon_path)
    canvas.create_image(width / 2, height / 2, image=icon_photo)
    canvas.image = icon_photo

    canvas.bind("<Button-1>", lambda e: on_click(canvas, id))
    canvas.bind("<Enter>", lambda e: on_enter(canvas, shapes, factor))
    canvas.bind("<Leave>", lambda e: on_leave(canvas, shapes, factor))
    return canvas

def create_dial(parent, size, label_txt, subtitle_txt, default, min, max):
    canvas = tk.Canvas(parent, width=size, height=size*(3/2), bg="white", highlightthickness=0)
    label = tk.Label(canvas, text=label_txt, fg="black", font=("Default", 8, "bold"), bg="white")
    subtitle_txt = subtitle_txt.replace("<n>", str(default))
    subtitle = tk.Label(canvas, text=subtitle_txt, font=("Default", 8), bg="white")
    icon_photo = tk.PhotoImage(file="assets/dial.png")
    canvas.image = icon_photo
    
    canvas.create_window(24, 10, window=label)
    canvas.create_image(24, 38, image=icon_photo)
    canvas.create_window(24, 65, window=subtitle)
    canvas.pack()
    return canvas

def create_slider(parent, width, height, icon_path):
    canvas = tk.Canvas(parent, width=width, height=height, bg="white", highlightthickness=0)
    rect_width = width - 20
    rect_height = 3
    if "large" in icon_path:
        bar_height=6
        timeline_img = tk.PhotoImage(file="assets/timeline.png")
        canvas.create_image(width / 2, height / 2, image=timeline_img)
        canvas.image1 = timeline_img

    icon_photo = tk.PhotoImage(file=icon_path)
    canvas.create_rectangle((width - rect_width) / 2, (height - rect_height) / 2, rect_width + (width - rect_width) / 2, rect_height + (height - rect_height) / 2, fill="black", outline="")
    canvas.create_image(15, height / 2, image=icon_photo)
    canvas.image2 = icon_photo
    canvas.pack()
    return canvas

def create_textbox(parent, width, height, label_txt, default, color):
    canvas = tk.Canvas(parent, width=width, height=height+20, bg="white", highlightthickness=0)
    label = tk.Label(canvas, text=label_txt, fg="black", font=("Default", 8, "bold"), bg="white")
    input_box = tk.Entry(canvas, width=4, justify="center", fg="black", font=("Default", 12, "bold"), bg="light grey")
    input_box.insert(0, default)
    shapes = create_rounded_rect(canvas, 0, 20, width, height, color)
    
    canvas.create_window(36, 10, window=label)
    canvas.create_window(36, 36, window=input_box)
    canvas.pack()
    return canvas
