import argparse
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import sounddevice as sd
import psola
import threading
import random
from functools import partial
from pedalboard import Pedalboard, Reverb, Delay, Compressor, Distortion
#After recording a snippet, audio will be saved to a file in 'ActuallyAwesomeAutotuner/raw.wav'
#This file may then be autotuned and saved under 'ActuallyAwesomeAutotuner/tuned.wav'
#If tuning is on, then 'tuned.wav' is loaded in memory for playback, o/w 'raw.wav' will be.
#Adding onto an existing recording will add to 'raw.wav' and 'tuned.wav' will regenerate
#Loading a saved recording will import it as 'raw.wav' and tuned material cannot be toggled

#Sound device defaults
sd.default.samplerate = 44100
sd.default.device = 0 #Device is id-based; check for devices by calling the function sd.query_devices()

#Global variables
mute = False
volume = 1
speed = 1.0
mic_pressed = False
y = []
sr = 44100
recording_thread = None
recording_started = False
decibels_L,decibels_R = -60,-60
devices = sd.query_devices()
input_devices = [device['name'] for device in devices if device['max_input_channels'] > 0]
output_devices = [device['name'] for device in devices if device['max_output_channels'] > 0]
meters = []

#NOTE: 'y' represents the audio file data, 'sr' is the sample rate of y

def open_file(filepath):
    return librosa.load(filepath, sr=None, mono=True)
#usage: y, sr = open_file(filepath)

def save_audio():
    global y
    if y is None:
        messagebox.showerror("Error", "No audio recorded yet!")
        return

    # Prompt the user to save the file using a file dialog
    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])

    if file_path:
        # Save the audio to the selected file
        write(file_path, fr, y)
        messagebox.showinfo("Success", f"Audio saved to {file_path}")

def change_speed(y, new_speed):
    y = librosa.effects.time_stretch(y, (new_speed / speed))
    speed = new_speed

def change_volume(y, new_volume):
    y *= (new_volume / volume)
    volume = new_volume

def play_audio(y, sr):
    global volume
    sd.play(y * volume, sr)

def mute_audio():
    global mute 
    mute = not mute
    if mute:
        print("Muted")
    else:
        print("Unmuted")

def stop_audio():
    sd.stop()

def rms_to_db(rms):
    return 20 * np.log10(rms) if rms > 0 else -60

def record_callback(indata, frames, time, status):
    """Callback function for recording audio."""
    global decibels_L,decibels_R
    if status:
        print(status)
    if not mute:  # Check if mute is off before appending data
        y.append(indata.copy())
        # Get the left channel and right channel deciebels respectively
        rms_L = np.sqrt(np.mean(indata[:,0]**2))
        decibels_L = rms_to_db(rms_L)
        rms_R = np.sqrt(np.mean(indata[:,1]**2))
        decibels_R = rms_to_db(rms_R)
        #Code below is for debugging purposes
        #decibels_L = random.randint(-60,0)
        #decibels_R = random.randint(-60,0)
        #print(decibels_L,decibels_R)
    else:
        # Append zeros instead of actual audio to keep the buffer length consistent
        y.append(np.zeros_like(indata))
        decibels_L,decibels_R=-60,-60

def record_audio(callback=None):
    global mic_pressed, recording_started, y, recording_thread, decibels_L, decibels_R

    if not recording_started:
        # Start recording
        y = []  # Reset the recording buffer (for now)
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

        # Save the recording
        if y:
            y = np.concatenate(y, axis=0)  # Concatenate the recorded frames
            sf.write('raw.wav', y, sd.default.samplerate)
            print("Recording saved as 'raw.wav'.")

        if callback:
            callback()

def get_decibels():
    return decibels_L, decibels_R

def closest_pitch(f0):
    midi_note = np.around(librosa.hz_to_midi(f0))
    nan_indices = np.isnan(f0)
    midi_note[nan_indices] = np.nan
    return librosa.midi_to_hz(midi_note)

def shift_pitch(n_steps):
    if n_steps!=0:
        y, sr = librosa.load("tuned.wav", sr=None, mono=True)
        shift_y = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
        sf.write('fx.wav', shift_y, sr)

def add_reverb(room_size):
    if room_size>0:
        y,sr = librosa.load("tuned.wav", sr=None, mono=True)
        board = Pedalboard([Reverb(room_size=room_size)])
        y_reverb = board(y, sr)
        sf.write('fx.wav', y_reverb, sr)
        print("Added reverb")
    pass

def add_delay(delay_seconds):
    if delay_seconds>0:
        y,sr = librosa.load("tuned.wav", sr=None, mono=True)
        board = Pedalboard([Delay(delay_seconds=delay_seconds)])
        y_delay = board(y, sr)
        sf.write('fx.wav', y_delay, sr)
        print("Added delay")

def add_compression(threshold):
    if threshold>0:
        y,sr = librosa.load("tuned.wav", sr=None, mono=True)
        board = Pedalboard([Compressor(threshold_db=threshold)])
        y_compress = board(y, sr)
        sf.write('fx.wav', y_compress, sr)
        print("Audio compressed")

def add_distortion(drive):
    if drive>0:
        y,sr = librosa.load("tuned.wav", sr=None, mono=True)
        board = Pedalboard([Distortion(drive_db=drive)])
        y_distort = board(y, sr)
        sf.write('fx.wav', y_distort, sr)
        print("Added distortion")

def autotune(_=None):
    y, sr = librosa.load("raw.wav", sr=None, mono=True)

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

    corrected_f0 = closest_pitch(f0)
    tuned_y = psola.vocode(y, sample_rate=int(sr), target_pitch=corrected_f0, fmin=fmin, fmax=fmax)
    sf.write("tuned.wav", tuned_y, sr)