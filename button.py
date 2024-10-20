import tkinter as tk

def create_button(parent, width, height, color, icon_path):
    radius = 15
    offset = 3
    canvas = tk.Canvas(parent, width=width, height=height)

    # Draw rounded rectangle
    canvas.create_oval(offset, offset, offset + radius, offset + radius, fill=color, outline="")
    canvas.create_oval(offset + width - radius, offset, offset + width, offset + radius, fill=color, outline="")
    canvas.create_oval(offset, offset + height - radius, offset + radius, offset + height, fill=color, outline="")
    canvas.create_oval(offset + width - radius, offset + height - radius, offset + width, offset + height, fill=color, outline="")
    canvas.create_rectangle(offset + radius / 2, offset, offset + width - radius / 2, offset + height, fill=color, outline="")
    canvas.create_rectangle(offset, offset + radius / 2, offset + width, offset + height - radius / 2, fill=color, outline="")

    # Add the icon to the canvas
    icon_photo = tk.PhotoImage(file=icon_path)
    canvas.create_image(width / 2, height / 2, image=icon_photo)

    # Keep a reference to avoid garbage collection
    canvas.image = icon_photo

    canvas.bind("<Button-1>", lambda e: print("Button clicked!"))
    canvas.pack()

# Create main window
root = tk.Tk()

# Create the rounded button with an icon
create_button(root, 100, 100, "light grey", "assets/volume.png")

# Run the application
root.mainloop()

