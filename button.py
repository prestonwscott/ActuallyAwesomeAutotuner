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

def create_button(parent, width, height, color, bgcolor, icon_path, factor=0.7):
    if len(bgcolor) == 0:
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    else:
        canvas = tk.Canvas(parent, width=width, height=height, bg=bgcolor, highlightthickness=0)
    shapes = create_rounded_rect(canvas, 0, 0, width, height, color)
    icon_photo = tk.PhotoImage(file=icon_path)
    canvas.create_image(width / 2, height / 2, image=icon_photo)
    canvas.image = icon_photo

    canvas.bind("<Button-1>", lambda e: print("Button clicked!"))
    canvas.bind("<Enter>", lambda e: on_enter(canvas, shapes, factor))
    canvas.bind("<Leave>", lambda e: on_leave(canvas, shapes, factor))
    return canvas

def create_dial(parent, size, label_txt, subtitle_txt, default, min, max):
    canvas = tk.Canvas(parent, width=size, height=size*(3/2), bg="white", highlightthickness=0)
    label = tk.Label(canvas, text=label_txt, font=("Default", 8, "bold"), bg="white")
    subtitle_txt = subtitle_txt.replace("<n>", str(default))
    subtitle = tk.Label(canvas, text=subtitle_txt, font=("Default", 8), bg="white")
    icon_photo = tk.PhotoImage(file="assets/dial.png")
    canvas.image = icon_photo
    
    canvas.create_window(24, 10, window=label)
    canvas.create_image(24, 38, image=icon_photo)
    canvas.create_window(24, 65, window=subtitle)
    canvas.pack()
    return canvas

def create_textbox(parent, width, height, label_txt, default, color):
    canvas = tk.Canvas(parent, width=width, height=height+20, bg="white", highlightthickness=0)
    label = tk.Label(canvas, text=label_txt, font=("Default", 8, "bold"), bg="white")
    input_box = tk.Entry(canvas, width=4, justify="center", font=("Default", 12, "bold"), bg="light grey")
    input_box.insert(0, default)
    shapes = create_rounded_rect(canvas, 0, 20, width, height, color)
    
    canvas.create_window(36, 10, window=label)
    canvas.create_window(36, 36, window=input_box)
    canvas.pack()
    return canvas

# Create main window
root = tk.Tk()

frame_content = tk.Frame(root)
frame_config = tk.Frame(frame_content)
panel_tune = create_panel(frame_config, 100, 216, "white", "")
panel_tune.grid(column=0, row=0)
button_tune = create_button(panel_tune, 48, 48, "light grey", "white", "assets/tunefork.png")
button_tune.place(x=26, y=8)
dial_gain = create_dial(panel_tune, 50, "Gain", "<n> dB", 0.0, -36.0, 36.0)
dial_gain.place(x=26, y=62)
dial_strength = create_dial(panel_tune, 50, "Strength", "<n>%", 50, 0, 100)
dial_strength.place(x=26, y=138)

panel_metro = create_panel(frame_config, 100, 178, "white", "")
panel_metro.grid(column=0, row=1, pady=8)
button_metro = create_button(panel_metro, 48, 48, "light grey", "white", "assets/metronome.png")
button_metro.place(x=26, y=8)
textbox_tempo = create_textbox(panel_metro, 72, 32, "Tempo", 120, "light grey")
textbox_tempo.place(x=14, y=62)
textbox_signature = create_textbox(panel_metro, 72, 32, "Signature", "4 / 4", "light grey")
textbox_signature.place(x=14, y=122)

panel_speed = create_panel(frame_config, 100, 140, "white", "")
panel_speed.grid(column=0, row=2)
button_speed = create_button(panel_speed, 48, 48, "light grey", "white", "assets/timer.png")
button_speed.place(x=26, y=8)
dial_speed = create_dial(panel_speed, 50, "Speed", "x<n>", 1.0, -4, 4)
dial_speed.place(x=26, y=62)
frame_config.grid(column=0, row=0)

button_microphone = create_button(frame_content, 250, 550, "light grey", "", "assets/microphone.png")
button_microphone.grid(column=1, row=0, padx=32, pady=16)

panel_reader = create_panel(frame_content, 100, 550, "white", "assets/decibelbar.png")
panel_reader.grid(column=2, row=0)
frame_content.grid(column=0, row=0)

frame_playback = create_panel(root, 560, 160, "white", "")
frame_playback.grid(column=0, row=1)


# Run the application
root.mainloop()

