import tkinter as tk
from .utils import *
from tkinter import StringVar, Label, OptionMenu

#Default colors
panel_color = "white"
#window_color = "#f0f0f0"
window_color = "red"
button_toggled = "light grey"
button_untoggled = "white"
button_hover = "grey"

def on_click(parent=None, id="None"):
    if parent is not None:
        change_color(parent)

    if(id == "Tuner toggle"):
        global tuner_enabled 
        tuner_enabled = not tuner_enabled
    
    if(id == "Metronome toggle"):
        global metronome_enabled 
        metronome_enabled = not metronome_enabled

    if(id == "Speed toggle"):
        global speed_enabled
        speed_enabled = not speed_enabled

    if(id == "Microphone toggle"):
        record_audio()

    if(id == "Mute toggle"):
        global mic_mute_enabled
        mic_mute_enabled = not mic_mute_enabled

    if(id == "Skip back"):
        pass
    
    if(id == "Rewind"):
        pass

    if(id == "Play"):
        pass

    if(id == "Fast forward"):
        pass
        
    if(id == "Skip forward"):
        pass
    
    if(id == "Extend file"):
        global extend_file_enabled
        extend_file_enabled = not extend_file_enabled

    if(id == "Volume mute toggle"):
        global vol_mute_enabled
        vol_mute_enabled = not vol_mute_enabled

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
    if parent_color == "SystemButtonFace":
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

def create_panel(parent, width, height, icon_path=None, include_meter=False):
    global dynamic_canvas,meters
    frame = tk.Frame(parent)
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

def create_button(parent, width, height, id, toggled=False, icon_path=None, text=None):
    parent_color = get_parent_color(parent)
    canvas = tk.Canvas(parent, width=width, height=height, bg=parent_color, highlightthickness=0)
    create_rounded_rect(canvas, 0, 0, width, height, button_toggled if toggled else button_untoggled)
    if icon_path is not None:
        icon_photo = tk.PhotoImage(file=icon_path)
        canvas.create_image(width / 2, height / 2, image=icon_photo)
        canvas.image = icon_photo
    elif text is not None:
        label = tk.Label(canvas, text=text, fg="black", font=("Default", 8, "bold"), bg=parent_color)
        canvas.create_window(24, 10, window=label)

    canvas.bind("<Button-1>", lambda e: on_click(parent=canvas, id=id))
    canvas.bind("<Enter>", lambda e: on_enter(parent=canvas))
    canvas.bind("<Leave>", lambda e: on_leave(parent=canvas))
    return canvas

def create_dial(parent, size, label_txt, subtitle_txt, default, min, max):
    parent_color = get_parent_color(parent)
    canvas = tk.Canvas(parent, width=size, height=size*(3/2), bg=parent_color, highlightthickness=0)
    label = tk.Label(canvas, text=label_txt, fg="black", font=("Default", 8, "bold"), bg=parent_color)
    subtitle_txt = subtitle_txt.replace("<n>", str(default))
    subtitle = tk.Label(canvas, text=subtitle_txt, fg="black", font=("Default", 8), bg=parent_color)
    icon_photo = tk.PhotoImage(file="assets/dial.png")
    canvas.image = icon_photo
    
    canvas.create_window(24, 10, window=label)
    canvas.create_image(24, 38, image=icon_photo)
    canvas.create_window(24, 65, window=subtitle)
    canvas.pack()
    return canvas

def create_slider(parent, width, height, icon_path):
    parent_color = get_parent_color(parent)
    canvas = tk.Canvas(parent, width=width, height=height, bg=parent_color, highlightthickness=0)
    rect_width = width - 20
    rect_height = 3
    if "large" in icon_path:
        bar_height=6
        #timeline_img = tk.PhotoImage(file="assets/timeline.png")
        #canvas.create_image(width / 2, height / 2, image=timeline_img)
        #canvas.image1 = timeline_img

    icon_photo = tk.PhotoImage(file=icon_path)
    canvas.create_rectangle((width - rect_width) / 2, (height - rect_height) / 2, rect_width + (width - rect_width) / 2, rect_height + (height - rect_height) / 2, fill="black", outline="")
    canvas.create_image(15, height / 2, image=icon_photo)
    canvas.image2 = icon_photo
    canvas.pack()
    return canvas

def create_textbox(parent, width, height, label_txt, default):
    parent_color = get_parent_color(parent)
    canvas = tk.Canvas(parent, width=width, height=height+20, bg=parent_color, highlightthickness=0)
    label = tk.Label(canvas, text=label_txt, fg="black", font=("Default", 8, "bold"), bg=parent_color)
    input_box = tk.Entry(canvas, width=4, justify="center", fg="black", font=("Default", 12, "bold"), bg=button_toggled)
    input_box.insert(0, default)
    shapes = create_rounded_rect(canvas, 0, 20, width, height, button_toggled)
    
    canvas.create_window(36, 10, window=label)
    canvas.create_window(36, 36, window=input_box)
    canvas.pack()
    return canvas