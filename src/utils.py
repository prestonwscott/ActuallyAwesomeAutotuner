import argparse
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import sounddevice as sd
import psola
from functools import partial

#After recording a snippet, audio will be saved to a file in 'ActuallyAwesomeAutotuner/raw.wav'
#This file may then be autotuned and saved under 'ActuallyAwesomeAutotuner/tuned.wav'
#If tuning is on, then 'tuned.wav' is loaded in memory for playback, o/w 'raw.wav' will be.
#Adding onto an existing recording will add to 'raw.wav' and 'tuned.wav' will regenerate
#Loading a saved recording will import it as 'raw.wav' and tuned material cannot be toggled

#Sound device defaults
sd.default.samplerate = None
sd.default.device = None
sd.default.channels = 1

#NOTE: 'y' represents the audio file data, 'sr' is the sample rate of y

def open_file(filepath):
    return librosa.load(filepath, sr=None, mono=True)
#usage: y, sr = open_file(filepath)

def change_speed(y, old_n, new_n):
    y = librosa.effects.time_stretch(y, (new_n / old_n))

def change_volume(y, old_n, new_n):
    y *= (new_n / old_n)

def play_audio(y, sr):
    sd.play(y, sr)

def stop_audio():
    sd.stop()

def closest_pitch(f0):
    midi_note = np.around(librosa.hz_to_midi(f0))
    nan_indices = np.isnan(f0)
    midi_note[nan_indices] = np.nan
    return librosa.midi_to_hz(midi_note)

def autotune():
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


