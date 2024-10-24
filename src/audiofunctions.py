import sounddevice as sd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.io.wavfile import write

# Set frame rate
fr = 44100
# Duration of the recording in seconds
duration = 5 
# Global variable to store audio data
recorded_audio = None  

# Function to record audio
def record_audio():
    global recorded_audio
    print("Recording...")
    # Recording audio for duration * frame rate
    recorded_audio = sd.rec(int(duration * fr), samplerate=fr, channels=2, dtype='int16')
    # Wait until the recording is finished
    sd.wait()  
    print("Recording finished.")
    # Save audio as raw.wav
    write("raw.wav", fr, recorded_audio)
    return recorded_audio

# Function to save recorded audio
def save_audio():
    global recorded_audio
    if recorded_audio is None:
        messagebox.showerror("Error", "No audio recorded yet!")
        return

    # Prompt the user to save the file using a file dialog
    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])

    if file_path:
        # Save the audio to the selected file
        write(file_path, fr, recorded_audio)
        messagebox.showinfo("Success", f"Audio saved to {file_path}")