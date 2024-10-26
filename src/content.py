import tkinter as tk
from .lib import *

class Content(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #root = tk.Tk()
        frame_body = tk.Frame(self)
        frame_config = tk.Frame(frame_body)
        panel_tune = create_panel(frame_config, 100, 216, "white", "")
        panel_tune.grid(column=0, row=0)
        button_tune = create_button(panel_tune, 48, 48, "light grey", "white", "Tuner toggle", "assets/tunefork.png")
        button_tune.place(x=26, y=8)
        dial_gain = create_dial(panel_tune, 50, "Gain", "<n> dB", 0.0, -36.0, 36.0)
        dial_gain.place(x=26, y=62)
        dial_strength = create_dial(panel_tune, 50, "Strength", "<n>%", 50, 0, 100)
        dial_strength.place(x=26, y=138)

        panel_metro = create_panel(frame_config, 100, 178, "white", "")
        panel_metro.grid(column=0, row=1, pady=8)
        button_metro = create_button(panel_metro, 48, 48, "light grey", "white", "Metronome toggle", "assets/metronome.png")
        button_metro.place(x=26, y=8)
        textbox_tempo = create_textbox(panel_metro, 72, 32, "Tempo", 120, "light grey")
        textbox_tempo.place(x=14, y=62)
        textbox_signature = create_textbox(panel_metro, 72, 32, "Signature", "4 / 4", "light grey")
        textbox_signature.place(x=14, y=122)

        panel_speed = create_panel(frame_config, 100, 140, "white", "")
        panel_speed.grid(column=0, row=2)
        button_speed = create_button(panel_speed, 48, 48, "light grey", "white", "Speed toggle", "assets/timer.png")
        button_speed.place(x=26, y=8)
        dial_speed = create_dial(panel_speed, 50, "Speed", "x<n>", 1.0, -4, 4)
        dial_speed.place(x=26, y=62)
        frame_config.grid(column=0, row=0)

        button_microphone = create_button(frame_body, 250, 550, "light grey", "", "Microphone toggle", "assets/microphone.png")
        button_microphone.grid(column=1, row=0, padx=32, pady=16)

        panel_reader = create_panel(frame_body, 100, 550, "white", "assets/decibelbar.png", True)
        panel_reader.grid(column=2, row=0)
        frame_body.grid(column=0, row=0)

        frame_footer = create_panel(self, 560, 160, "white", "")
        frame_playback = tk.Frame(frame_footer, bg="white")
        button_mute = create_button(frame_playback, 34, 34, "white", "white", "Mute toggle", "assets/mute.png")
        button_mute.grid(column=0, row=0, padx=50, pady=16)
        button_skipback = create_button(frame_playback, 34, 34, "white", "white", "Skip back", "assets/skipback.png")
        button_skipback.grid(column=1, row=0, padx=4)
        button_rewind = create_button(frame_playback, 34, 34, "white", "white", "Rewind", "assets/rewind.png")
        button_rewind.grid(column=2, row=0, padx=4)
        button_playpause = create_button(frame_playback, 34, 34, "white", "white", "Play", "assets/play.png")
        button_playpause.grid(column=3, row=0, padx=20)
        button_fastforward = create_button(frame_playback, 34, 34, "white", "white", "Fast forward", "assets/fastforward.png")
        button_fastforward.grid(column=4, row=0, padx=4)
        button_skipforward = create_button(frame_playback, 34, 34, "white", "white", "Skip forward", "assets/skipforward.png")
        button_skipforward.grid(column=5, row=0, padx=4)
        button_extend = create_button(frame_playback, 34, 34, "white", "white", "Extend file", "assets/extend.png")
        button_extend.grid(column=6, row=0, padx=50)
        frame_playback.place(x=25, y=0)

        frame_timeline = tk.Frame(frame_footer, bg="white")
        slider_timeline = create_slider(frame_timeline, 500, 76, "assets/slidetoggle_large.png")
        frame_timeline.place(x=25, y=50)

        frame_volume = tk.Frame(frame_footer, bg="white")
        button_volume = create_button(frame_volume, 34, 34, "white", "white", "Volume mute toggle", "assets/volume.png")
        button_volume.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        slider_volume = create_slider(frame_volume, 160, 16, "assets/slidetoggle_small.png")
        slider_volume.pack(side=tk.RIGHT, anchor=tk.CENTER, expand=True)
        frame_volume.place(x=110, y=120)

        frame_progress = tk.Frame(frame_footer, bg="red")
        label_progress = tk.Label(frame_progress, text="0:05/0:47", fg="black", font=("Default", 14, "bold"), bg="white")
        label_progress.pack()
        frame_progress.place(x=340, y=120)
        frame_footer.grid(column=0, row=1)

#root.mainloop()
