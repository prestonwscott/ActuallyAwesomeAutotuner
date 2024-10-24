import argparse
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import sounddevice as sd
import psola
from functools import partial
import threading
#After recording a snippet, audio will be saved to a file in 'ActuallyAwesomeAutotuner/raw.wav'
#This file may then be autotuned and saved under 'ActuallyAwesomeAutotuner/tuned.wav'
#If tuning is on, then 'tuned.wav' is loaded in memory for playback, o/w 'raw.wav' will be.
#Adding onto an existing recording will add to 'raw.wav' and 'tuned.wav' will regenerate
#Loading a saved recording will import it as 'raw.wav' and tuned material cannot be toggled

#Sound device defaults
sd.default.samplerate = 44100
sd.default.device = None
sd.default.channels = 1

#Global variables
mute = False
volume = 1
mic_pressed = False
recording = []
recording_thread = None
recording_started = False

#NOTE: 'y' represents the audio file data, 'sr' is the sample rate of y

def open_file(filepath):
    return librosa.load(filepath, sr=None, mono=True)
#usage: y, sr = open_file(filepath)

def change_speed(y, old_n, new_n):
    y = librosa.effects.time_stretch(y, (new_n / old_n))

def change_volume(y, old_n, new_n):
    y *= (new_n / old_n)

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

def record_callback(indata, frames, time, status):
    """Callback function for recording audio."""
    if status:
        print(status)
    if not mute:  # Check if mute is off before appending data
        recording.append(indata.copy())
    else:
        # Append zeros instead of actual audio to keep the buffer length consistent
        recording.append(np.zeros_like(indata))

def record_audio(callback=None):
    global mic_pressed, recording_started, recording, recording_thread

    if not recording_started:
        # Start recording
        recording = []  # Reset the recording buffer
        mic_pressed = True
        recording_started = True
        
        print("Recording... Press the button again to stop.")

        # Start the audio input stream in a separate thread
        def start_stream():
            with sd.InputStream(callback=record_callback, channels=1, samplerate=sd.default.samplerate):
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

        # Save the recording
        if recording:
            recording = np.concatenate(recording, axis=0)  # Concatenate the recorded frames
            sf.write('raw.wav', recording, sd.default.samplerate)
            print("Recording saved as 'raw.wav'.")

        if callback:
            callback()

def closest_pitch(f0):
    midi_note = np.around(librosa.hz_to_midi(f0))
    nan_indices = np.isnan(f0)
    midi_note[nan_indices] = np.nan
    return librosa.midi_to_hz(midi_note)

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


