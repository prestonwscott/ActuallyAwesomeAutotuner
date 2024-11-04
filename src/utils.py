import argparse
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import sounddevice as sd
import psola
import random
import threading as t
import time
from tkinter import messagebox
from tkinter import filedialog
from tkinter import DoubleVar
from functools import partial
from pedalboard import Pedalboard, Reverb, Delay, Compressor, Distortion
from .globals import *

#NOTE: Loading a saved recording will import it and tuned material cannot be toggled.
#      'y' represents the numpy audio stream, 'sr' is the sample rate of y

def open_file():
    global y, sr, tuned_y, raw_y
    res = messagebox.askyesno("Open file", "This operation will override your existing audio, continue?")
    if res:
        filepath = filedialog.askopenfilename(title="Select a WAV file", filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
        if filepath:
            y, sr = librosa.load(filepath)
            tuned_y = None
            num_chunks = int(np.ceil(len(y) / sr))
            raw_y = []
            
            for i in range(num_chunks):
                start_index = i * sr
                end_index = start_index + sr
                raw_y.append(y[start_index:end_index])
    return res
    

def clear_file():
    global y, tuned_y, raw_y
    res = messagebox.askyesno("New file", "This operation will clear all audio, continue?")
    if res:
        y = None
        raw_y = None
        tuned_y = None
    return res

def save_audio():
    global y, tuned_y
    if y is None:
        messagebox.showwarning("Save file", "No audio recorded yet!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    if file_path:
        if tuner_enabled and tuned_y is not None:
            sf.write(file_path, tuned_y, sr)
        elif y is not None:
            sf.write(file_path, y, sr)
        messagebox.showinfo("Save file", f"Audio saved to {file_path}")

def get_duration():
    global y, sr
    if y is not None and sr is not None:
        tot_seconds = y.shape[0] / sr
        minutes = str(int(tot_seconds / 60))
        seconds = str(int(tot_seconds % 60))
        seconds = "0" + seconds if int(seconds) < 10 else seconds
        return str(minutes + ":" + seconds)
    return "0:00"


def change_speed(new_speed):
    global y, tuned_y, speed
    delta_speed = new_speed / (speed if speed > 0 else 1)
    if y is not None:
        y = librosa.effects.time_stretch(y, delta_speed)
    if tuned_y is not None:
        tuned_y = librosa.effects.time_stretch(tuned_y, delta_speed)
    speed = new_speed

def change_volume(new_volume):
    global y, tuned_y, volume
    delta_volume = new_volume / (volume if volume > 0 else 1)
    if y is not None:
        y *= delta_volume
    if tuned_y is not None:
        tuned_y *= delta_volume
    volume = new_volume

def play_metronome():
    global metronome_enabled
    duration = 0.1
    frequency = 440
    t = np.linspace(0, duration, int(sr * duration), False)
    beep = 0.5 * np.sin(2 * np.pi * frequency * t)
    if metronome_enabled:
        sd.play(beep, sr)

def play_audio():
    global y, tuned_y, volume, sr
    if tuner_enabled and tuned_y is not None:
        sd.play(tuned_y * volume, sr)
    elif y is not None:
        sd.play(y * volume, sr)

def stop_audio():
    sd.stop()

def rms_to_db(rms):
    return 20 * np.log10(rms) if rms > 0 else -60

def record_callback(indata, frames, time, status):
    global raw_y, decibels_L, decibels_R
    if status:
        print(status)
    if not mic_mute_enabled:
        raw_y.append(indata[:, 0].copy())

        if indata.shape[1] > 1:
            # Stereo: Process both left and right channels
            rms_L = np.sqrt(np.mean(indata[:, 0]**2))
            decibels_L = rms_to_db(rms_L)
            rms_R = np.sqrt(np.mean(indata[:, 1]**2))
            decibels_R = rms_to_db(rms_R)
        else:
            # Mono: Use the same channel for both left and right
            rms_L = np.sqrt(np.mean(indata[:, 0]**2))
            decibels_L = rms_to_db(rms_L)
            rms_R = np.sqrt(np.mean(indata[:, 0]**2))
            decibels_R = decibels_L
    else:
        # Append zeros instead of actual audio to keep the buffer length consistent
        raw_y.append(np.zeros_like(indata))
        decibels_L,decibels_R=-60,-60

def record_audio():
    global mic_pressed, recording_started, y, raw_y, met_thread, recording_thread, decibels_L, decibels_R
    if not recording_started:
        # Start recording
        y = None
        if raw_y is None or not extend_file_enabled:
            raw_y = []
        mic_pressed = True
        recording_started = True

        device_info = sd.query_devices(sd.default.device[0], 'input')
        num_channels = device_info['max_input_channels']
        if num_channels == 0:
            raise ValueError("No input channels available.")

        def start_stream():
            with sd.InputStream(callback=record_callback, channels=num_channels, samplerate=sd.default.samplerate):
                while recording_started:
                    sd.sleep(100)

        def start_metronome():
            while recording_started:
                global bpm
                play_metronome()
                time.sleep(60/bpm)

        recording_thread = t.Thread(target=start_stream)
        met_thread = t.Thread(target=start_metronome)
        recording_thread.start()
        met_thread.start()
    else:
        # Stop recording
        recording_started = False
        mic_pressed = False
        stop_audio()

        if recording_thread is not None and recording_thread._started:
            recording_thread.join()
            recording_thread = None
            decibels_L,decibels_R=-60,-60
        
        if met_thread is not None and met_thread._started:
                met_thread.join()
                met_thread = None

        if raw_y is not None and raw_y:
            y = np.concatenate(raw_y, axis=0)
            #y = np.mean(y, axis=1)

        t.Thread(target=autotune).start()

def bake_effects(new_reverb, new_delay, new_pitch, new_compression, new_distortion):
    global tuned_y, sr, reverb, delay, pitch, compression, distortion
    reverb = new_reverb
    delay = new_delay
    pitch = new_pitch
    compression = new_compression
    distortion = new_distortion
    if tuned_y is not None and ((reverb >= 0 and reverb <= 1) and (delay >= 0) and (pitch >= 0) and (compression >= 0) and (distortion >= 0)):
        board = Pedalboard([Reverb(room_size=reverb), Delay(delay_seconds=delay), Compressor(threshold_db=compression), Distortion(drive_db=distortion)])
        tuned_y = board(tuned_y, sr)
        tuned_y = librosa.effects.pitch_shift(tuned_y, sr=sr, n_steps=pitch)

def autotune():
    global y, sr, tuned_y
    frame_length = 2048
    hop_length = frame_length // 4
    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C7')
    f0, voiced_flag, voiced_probabilities = librosa.pyin(y,
                                                         frame_length=frame_length,
                                                         hop_length=hop_length,
                                                         sr=sr,
                                                         fmin=fmin,
                                                         fmax=fmax)

    midi_note = np.around(librosa.hz_to_midi(f0))
    nan_indices = np.isnan(f0)
    midi_note[nan_indices] = np.nan
    tuned_y = psola.vocode(y, sample_rate=int(sr), target_pitch=librosa.midi_to_hz(midi_note), fmin=fmin, fmax=fmax)
    
def get_decibels():
    return decibels_L, decibels_R

def toggle_play():
    global is_playing
    if not is_playing:
        play_audio()
    else:
        stop_audio()
    is_playing = not is_playing

def toggle_tuner():
    global tuner_enabled
    tuner_enabled = not tuner_enabled

def toggle_metro():
    global metronome_enabled
    metronome_enabled = not metronome_enabled

def toggle_speed():
    global speed_enabled
    speed_enabled = not speed_enabled

def toggle_mic_mute():
    global mic_mute_enabled
    mic_mute_enabled = not mic_mute_enabled

def toggle_extend():
    global extend_file_enabled
    extend_file_enabled = not extend_file_enabled

def toggle_vol_mute():
    global vol_mute_enabled
    vol_mute_enabled = not vol_mute_enabled

def set_volume(new_volume):
    global volume
    volume = new_volume

def set_speed(new_speed):
    global speed
    speed = new_speed

def set_bpm(new_bpm):
    global bpm
    bpm = new_bpm

def get_bpm():
    global bpm
    return bpm

def set_signature(new_signature):
    global signature
    signature = new_signature

def get_signature():
    global signature
    return signature