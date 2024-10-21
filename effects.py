import numpy as np
import sounddevice as sd
import soundfile as sf
from pyo import *

def read_soundfile(filename):
    return sf.read(filename)

def playback(data, fs):
    sd.play(data, fs)
    sd.wait()

def set_volume(stream):
    pass

def autotune_stream(stream):
    pass