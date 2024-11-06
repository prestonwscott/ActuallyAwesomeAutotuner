import tkinter as tk
import re
from .globals import *
from .utils import *
from tkinter import StringVar, Label, OptionMenu

def on_click(parent=None, progress=None):
    if parent is not None:
        change_color(parent)
    
    id = parent._name
    if(id == "tuner toggle"):
        toggle_tuner()
    
    elif(id == "metronome toggle"):
        toggle_metro()

    elif(id == "speed toggle"):
        toggle_speed()

    elif(id == "microphone toggle"):
        record_audio(progress)
        if progress is not None:
            progress.config(text="0:00/" + get_duration())

    elif(id == "mute toggle"):
        toggle_mic_mute()

    elif(id == "play"):
        global is_playing
        is_playing = not is_playing
        icon_path = "assets/play.png" if not is_playing else "assets/pause.png"
        icon_photo = tk.PhotoImage(file=icon_path)
        parent.create_image(int(parent.cget("width")) / 2, int(parent.cget("height")) / 2, image=icon_photo)
        parent.image = icon_photo
        toggle_play(progress)

    elif(id == "extend file"):
        toggle_extend()

def on_text_modified(parent):
    id = parent._name
    value = parent.get()
    if(id == "tempo"):
        if value.isdigit() and (int(value) >= 1 and int(value) <= 120):
            set_bpm(int(value))
        else:
            parent.delete(0, tk.END)
            parent.insert(0, str(get_bpm()))

def on_enter(parent):
    shapes = parent.find_all()
    for shape in shapes:
        if parent.type(shape) in ["rectangle", "oval", "line", "polygon", "arc"]:
            current_color = parent.itemcget(shape, "fill")
            if current_color == button_toggled:
                new_color = button_hover
            elif current_color == button_untoggled:
                new_color = button_toggled
            else:
                return
            parent.itemconfig(shape, fill=new_color)

def on_leave(parent):
    shapes = parent.find_all()
    for shape in shapes:
        if parent.type(shape) in ["rectangle", "oval", "line", "polygon", "arc"]:
            current_color = parent.itemcget(shape, "fill")
            if current_color == button_hover:
                new_color = button_toggled
            elif current_color == button_toggled:
                new_color = button_untoggled
            else:
                return
            parent.itemconfig(shape, fill=new_color)

def change_color(parent):
    shapes = parent.find_all()
    for shape in shapes:
        if parent.type(shape) in ["rectangle", "oval", "line", "polygon", "arc"]:
            current_color = parent.itemcget(shape, "fill")
            if current_color == button_hover:
                new_color = button_untoggled
            elif current_color == button_toggled:
                new_color = button_hover
            elif current_color == button_untoggled:
                new_color = button_hover
            else:
                return
            parent.itemconfig(shape, fill=new_color)

def get_parent_color(parent):
    parent_color = parent.cget("background")
    if "system" in parent_color.lower():
        return panel_color
    else:
        return parent_color

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

def create_panel(parent, width, height, icon_path=None, include_meter=False, name=None):
    global dynamic_canvas,meters
    frame = tk.Frame(parent, name=name)
    canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0, bg=window_color)
    create_rounded_rect(canvas, 0, 0, width, height, panel_color)
    if icon_path is not None:
        icon_photo = tk.PhotoImage(file=icon_path)
        canvas.create_image(width / 2, height / 2, image=icon_photo)
        canvas.image = icon_photo
    
    if include_meter==True:
        left_meter = canvas.create_rectangle(10, height-17, 34, height-17, fill='light green', outline='')
        right_meter = canvas.create_rectangle(38, height-17, 62, height-17, fill='light green', outline='')
        meters.append(left_meter)
        meters.append(right_meter)
        dynamic_canvas = canvas
    canvas.pack()
    return frame

def get_dynamic_canvas():
    return dynamic_canvas

def get_meters():
    return meters

def create_button(parent, width, height, id, toggled=False, icon_path=None, text=None, progress=None):
    parent_color = get_parent_color(parent)
    canvas = tk.Canvas(parent, width=width, height=height, bg=parent_color, highlightthickness=0, name=id.lower())
    create_rounded_rect(canvas, 0, 0, width, height, button_toggled if toggled else button_untoggled)
    if icon_path is not None:
        icon_photo = tk.PhotoImage(file=icon_path)
        canvas.create_image(width / 2, height / 2, image=icon_photo)
        canvas.image = icon_photo
    elif text is not None:
        label = tk.Label(canvas, text=text, fg="black", font=("Default", 8, "bold"), bg=parent_color)
        canvas.create_window(24, 10, window=label)

    canvas.bind("<Button-1>", lambda e: on_click(parent=canvas, progress=progress))
    canvas.bind("<Enter>", lambda e: on_enter(parent=canvas))
    canvas.bind("<Leave>", lambda e: on_leave(parent=canvas))
    return canvas

def create_textbox(parent, width, height, label_txt, default):
    parent_color = get_parent_color(parent)
    canvas = tk.Canvas(parent, width=width, height=height+20, bg=parent_color, highlightthickness=0)
    label = tk.Label(canvas, text=label_txt, fg="black", font=("Default", 8, "bold"), bg=parent_color)
    input_box = tk.Entry(canvas, width=4, justify="center", fg="black", font=("Default", 12, "bold"), bg=button_toggled, name=label_txt.lower())
    input_box.insert(0, default)
    shapes = create_rounded_rect(canvas, 0, 20, width, height, button_toggled)
    
    canvas.create_window(36, 10, window=label)
    canvas.create_window(36, 36, window=input_box)
    input_box.bind("<FocusOut>", lambda e: on_text_modified(parent=input_box))
    canvas.pack()
    return canvas
