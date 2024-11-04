import tkinter as tk
from .lib import *
from .globals import *

class Content(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        frame_master = tk.Frame(self, bg=window_color, name="frame_master")
        frame_body = tk.Frame(frame_master, bg=window_color)
        frame_config = tk.Frame(frame_body, bg=window_color)
        panel_tune = create_panel(frame_config, 100, 216)
        panel_tune.grid(column=0, row=0)
        button_tune = create_button(panel_tune, 48, 48, "Tuner toggle", toggled=tuner_enabled, icon_path="assets/tunefork.png")
        button_tune.place(x=26, y=8)
        dial_gain = create_dial(panel_tune, 50, "Gain", "<n> dB", 0.0, -36.0, 36.0)
        dial_gain.place(x=26, y=62)
        dial_strength = create_dial(panel_tune, 50, "Strength", "<n>%", 50, 0, 100)
        dial_strength.place(x=26, y=138)

        panel_metro = create_panel(frame_config, 100, 178)
        panel_metro.grid(column=0, row=1, pady=8)
        button_metro = create_button(panel_metro, 48, 48, "Metronome toggle", toggled=metronome_enabled, icon_path="assets/metronome.png")
        button_metro.place(x=26, y=8)
        textbox_tempo = create_textbox(panel_metro, 72, 32, "Tempo", bpm)
        textbox_tempo.place(x=14, y=62)
        textbox_signature = create_textbox(panel_metro, 72, 32, "Signature", signature)
        textbox_signature.place(x=14, y=122)

        panel_speed = create_panel(frame_config, 100, 140)
        panel_speed.grid(column=0, row=2)
        button_speed = create_button(panel_speed, 48, 48, "Speed toggle", toggled=speed_enabled, icon_path="assets/timer.png")
        button_speed.place(x=26, y=8)
        dial_speed = create_dial(panel_speed, 50, "Speed", "x<n>", 1.0, -4, 4)
        dial_speed.place(x=26, y=62)
        frame_config.grid(column=0, row=0,)

        panel_reader = create_panel(frame_body, 100, 550, icon_path="assets/decibelbar.png", include_meter=True)
        panel_reader.grid(column=2, row=0)
        frame_body.grid(column=0, row=0)

        frame_footer = create_panel(frame_master, 560, 160, name="frame_footer")
        frame_playback = tk.Frame(frame_footer, bg=panel_color)
        button_mute = create_button(frame_playback, 34, 34, "Mute toggle", toggled=mic_mute_enabled, icon_path="assets/mute.png")
        button_mute.grid(column=0, row=0, padx=50, pady=16)
        button_skipback = create_button(frame_playback, 34, 34, "Skip back", toggled=is_sb, icon_path="assets/skipback.png")
        button_skipback.grid(column=1, row=0, padx=4)
        button_rewind = create_button(frame_playback, 34, 34, "Rewind", toggled=is_rw, icon_path="assets/rewind.png")
        button_rewind.grid(column=2, row=0, padx=4)
        button_fastforward = create_button(frame_playback, 34, 34, "Fast forward", toggled=is_ff, icon_path="assets/fastforward.png")
        button_fastforward.grid(column=4, row=0, padx=4)
        button_skipforward = create_button(frame_playback, 34, 34, "Skip forward", toggled=is_sf, icon_path="assets/skipforward.png")
        button_skipforward.grid(column=5, row=0, padx=4)
        button_extend = create_button(frame_playback, 34, 34, "Extend file", toggled=extend_file_enabled, icon_path="assets/extend.png")
        button_extend.grid(column=6, row=0, padx=50)
        frame_playback.place(x=25, y=0)

        frame_timeline = tk.Frame(frame_footer, bg=panel_color)
        slider_timeline = create_slider(frame_timeline, 500, 76, "assets/slidetoggle_large.png")
        frame_timeline.place(x=25, y=50)

        frame_volume = tk.Frame(frame_footer, bg=panel_color)
        button_volume = create_button(frame_volume, 34, 34, "Volume mute toggle", toggled=vol_mute_enabled, icon_path="assets/volume.png")
        button_volume.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        slider_volume = create_slider(frame_volume, 160, 16, "assets/slidetoggle_small.png")
        slider_volume.pack(side=tk.RIGHT, anchor=tk.CENTER, expand=True)
        frame_volume.place(x=110, y=120)

        frame_progress = tk.Frame(frame_footer, bg=panel_color, name="frame_progress")
        label_progress = tk.Label(frame_progress, text="0:00/0:00", fg="black", font=("Default", 14, "bold"), bg=panel_color, name="label_progress")
        label_progress.pack()
        frame_progress.place(x=340, y=120)
        frame_footer.grid(column=0, row=1)

        button_microphone = create_button(frame_body, 250, 550, "Microphone toggle", toggled=recording_started, icon_path="assets/microphone.png", progress=label_progress)
        button_microphone.grid(column=1, row=0, padx=32, pady=16)

        button_playpause = create_button(frame_playback, 34, 34, "Play", toggled=is_playing, icon_path="assets/play.png", progress=label_progress)
        button_playpause.grid(column=3, row=0, padx=20)
        frame_master.pack()

class Effect(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame_body = tk.Frame(self)
        padding_y = 30

        room_size = tk.DoubleVar(value=0)
        reverb_label = tk.Label(frame_body, text="Reverb",  font=("Default", 12, "bold"))
        reverb_label.grid(column=0, row=0)
        reverb_entry = tk.Entry(frame_body, width=3, textvariable=room_size, font=("Default", 10))
        reverb_entry.grid(column=1, row=0)
        reverb_size = tk.Label(frame_body, text="room size (0-1)", font=("Default", 10))
        reverb_size.grid(column=2, row=0, pady=padding_y)
        
        pitch = tk.IntVar(value=0)
        pitch_label = tk.Label(frame_body, text="Pitch", font=("Default", 12, "bold"))
        pitch_label.grid(column=0, row=2)
        pitch_entry = tk.Entry(frame_body, width=3, textvariable=pitch, font=("Default", 10))
        pitch_entry.grid(column=1, row=2)
        pitch_steps = tk.Label(frame_body, text="steps", font=("Default", 10))
        pitch_steps.grid(column=2, row=2, pady=padding_y)

        delay = tk.IntVar(value=0)
        delay_label = tk.Label(frame_body, text="Delay", font=("Default", 12, "bold"))
        delay_label.grid(column=0, row=1)
        delay_entry = tk.Entry(frame_body, width=3, textvariable=delay, font=("Default", 10))
        delay_entry.grid(column=1, row=1)
        delay_seconds = tk.Label(frame_body, text="delay (in s)", font=("Default", 10))
        delay_seconds.grid(column=2, row=1, pady=padding_y)
        
        th = tk.DoubleVar(value=0)
        compressor_label = tk.Label(frame_body, text="Compressor", font=("Default", 12, "bold"))
        compressor_label.grid(column=0, row=3)
        compressor_entry = tk.Entry(frame_body, textvariable=th, width=3, font=("Default", 10))
        compressor_entry.grid(column=1, row=3)
        compressor_th = tk.Label(frame_body, text="thresehold (dB)", font=("Default", 10))
        compressor_th.grid(column=2, row=3, pady=padding_y)

        drive_db = tk.DoubleVar(value=0)
        distortion_label = tk.Label(frame_body, text="Distortion", font=("Default", 12, "bold"))
        distortion_label.grid(column=0, row=4)
        distortion_entry = tk.Entry(frame_body, textvariable=drive_db, width=3, font=("Default", 10))
        distortion_entry.grid(column=1, row=4)
        distortion_drive = tk.Label(frame_body, text="drive (dB)", font=("Default", 10))
        distortion_drive.grid(column=2, row=4, pady=padding_y)
        
        save_button = tk.Button(frame_body, text="Apply effects", command=lambda: bake_effects(room_size.get(),delay.get(),pitch.get(),th.get(),drive_db.get()))
        save_button.grid(column=1, row=5, pady=padding_y)
        frame_body.pack()

class Devices(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame_body = tk.Frame(self)
        padding_y = 30
    
        input_label = Label(frame_body, text="Select Input Device:", font=("Default", 12, "bold"))
        input_label.grid(column=0, row=0)
        
        input_device_var = StringVar()
        input_device_var.set(input_devices[0] if input_devices else "No input device found")
        input_device_dropdown = OptionMenu(frame_body, input_device_var, *input_devices)
        input_device_dropdown.grid(column=0, row=1, pady=padding_y)
        
        output_label = Label(frame_body, text="Select Output Device:", font=("Default", 12, "bold"))
        output_label.grid(column=0, row=2, pady=(padding_y, 0))
        
        output_device_var = StringVar()
        output_device_var.set(output_devices[0] if output_devices else "No output device found")
        output_device_dropdown = OptionMenu(frame_body, output_device_var, *output_devices)
        output_device_dropdown.grid(column=0, row=3, pady=padding_y)
        
        def save_device_selection():
            sd.default.device = (all_devices.index(input_device_var.get()), all_devices.index(output_device_var.get()))

        save_button = tk.Button(frame_body, text="Save Selection", command=save_device_selection)
        save_button.grid(column=0, row=4, pady=padding_y)
        frame_body.pack()