import sounddevice as sd

#Default colors
panel_color = "white"
window_color = "#f0f0f0"
button_toggled = "light grey"
button_untoggled = "white"
button_hover = "grey"

#Sound device defaults
sd.default.samplerate = 44100
sd.default.device = 1

#Recording info
mic_pressed = False
y = None
raw_y = None
tuned_y = None
sr = sd.default.samplerate
recording_thread = None
met_thread = None
recording_started = False
progress_started = False
decibels_L,decibels_R = -60,-60
devices = sd.query_devices()
all_devices = [device['name'] for device in devices]
input_devices = [device['name'] for device in devices if device['max_input_channels'] > 0 and device['max_input_channels'] < 3]
output_devices = [device['name'] for device in devices if device['max_output_channels'] > 0 and device['max_output_channels'] < 3]
meters = []
progress_thread = None

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
bpm = 60
timer_s = 0

#Playback values
is_sb = False
is_rw = False
is_playing = False
is_ff = False
is_sf = False
