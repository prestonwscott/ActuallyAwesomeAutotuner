import argparse
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import sounddevice as sd
import psola
import threading
import random
import threading as t
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
from pedalboard import Pedalboard, Reverb, Delay, Compressor, Distortion
#NOTE: Loading a saved recording will import it and tuned material cannot be toggled.
#      'y' represents the numpy audio stream, 'sr' is the sample rate of y

#Sound device defaults
sd.default.samplerate = 44100
sd.default.device = 0

#Recording info
mic_pressed = False
y = None
raw_y = None
tuned_y = None
sr = sd.default.samplerate
recording_thread = None
recording_started = False
decibels_L,decibels_R = -60,-60
devices = sd.query_devices()
all_devices = [device['name'] for device in devices]
input_devices = [device['name'] for device in devices if device['max_input_channels'] > 0]
output_devices = [device['name'] for device in devices if device['max_output_channels'] > 0]
meters = []

#Toggle values
tuner_enabled = True
metronome_enabled = True
speed_enabled = False
mic_mute_enabled = False
extend_file_enabled = False
vol_mute_enabled = False

#Control values
volume = 1
speed = 1.0
reverb = 0
pitch = 0
delay = 0
compression = 0
distortion = 0

#Playback values
is_sb = False
is_rw = False
is_playing = False
is_ff = False
is_sf = False

def open_file(filepath):
    global y, sr
    y, sr = librosa.load(filepath)

def save_audio():
    global y, tuned_y
    if y is None:
        messagebox.showwarning("Save File", "No audio recorded yet!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    if file_path:
        if tuner_enabled and tuned_y is not None:
            sf.write(file_path, tuned_y, sr)
        elif y is not None:
            sf.write(file_path, y, sr)
        messagebox.showinfo("Save File", f"Audio saved to {file_path}")
    
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

def play_audio():
    global y, tuned_y, volume, sr, tuner_enabled
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
        raw_y.append(indata.copy())

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
        y.append(np.zeros_like(indata))
        decibels_L,decibels_R=-60,-60

def record_audio():
    global mic_pressed, recording_started, y, raw_y, recording_thread, decibels_L, decibels_R
    if not recording_started:
        # Start recording
        if raw_y is None or not extend_file_enabled:
            raw_y = []
        mic_pressed = True
        recording_started = True

        device_info = sd.query_devices(sd.default.device[0], 'input')
        num_channels = device_info['max_input_channels']
        if num_channels == 0:
            raise ValueError("No input channels available.")
        
        print("Recording... Press the button again to stop.")

        # Start the audio input stream in a separate thread
        def start_stream():
            with sd.InputStream(callback=record_callback, channels=num_channels, samplerate=sd.default.samplerate):
                while recording_started:
                    sd.sleep(100)  # Keep the stream open

        recording_thread = threading.Thread(target=start_stream)
        recording_thread.start()
    else:
        # Stop recording
        recording_started = False
        mic_pressed = False
        stop_audio()

        # Wait for the recording thread to finish, if it exists
        if recording_thread is not None:
            recording_thread.join()
            recording_thread = None  # Reset the thread variable
            decibels_L,decibels_R=-60,-60

        if raw_y is not None and raw_y:
            y = np.concatenate(raw_y, axis=0)
            y = np.mean(y, axis=1)

        if tuner_enabled:
             autotune()

def get_decibels():
    return decibels_L, decibels_R

def bake_effects(new_reverb, new_delay, new_pitch, new_compression, new_distortion):
    global tuned_y, sr, reverb, delay, pitch, compression, distortion
    delta_reverb = new_reverb / (reverb if reverb > 0 else 1)
    delta_delay = new_delay / (delay if delay > 0 else 1)
    delta_pitch = new_pitch / (pitch if pitch > 0 else 1)
    delta_compression = new_compression / (compression if compression > 0 else 1)
    delta_distortion = new_distortion / (distortion if distortion > 0 else 1)
    if tuned_y is not None and ((delta_reverb > 0 and delta_reverb < 1) and (delta_delay > 0) and (delta_pitch > 0) and (delta_compression > 0) and (delta_distortion > 0)):
        board = Pedalboard([Reverb(room_size=delta_reverb), Delay(delay_seconds=delta_delay), Compressor(threshold_db=delta_compression), Distortion(drive_db=delta_distortion)])
        tuned_y = board(tuned_y, sr)
        tuned_y = librosa.effects.pitch_shift(tuned_y, sr=sr, n_steps=delta_pitch)
        reverb = new_reverb
        delay = new_delay
        pitch = new_pitch
        compression = new_compression
        distortion = new_distortion

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
    play_audio()
