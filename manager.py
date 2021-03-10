import audioop
import pyaudio
from subprocess import Popen
from time import time

####
# manager.py by Different55 <burritosaur@protonmail.com>
# Manages the running of other blinkstick visualization scripts. Currently only
# Checks if audio is playing to choose between launching lavalamp or blinkpulse,
# but in the future will also provide information about the weather in the
# morning (sky.py and storm.py) as well as picking idle animations at night from
# fire.py, fireflies.py, and stars.py.
####

chunk = 1024
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=chunk
)

currently_visualizing = False
v = Popen(["python", "lavalamp.py"])

while True:
    data = stream.read(chunk)
    rms = audioop.rms(data, 2)  # Get volume of currently playing audio.

    if (
        currently_visualizing and rms == 0
    ):  # If we're visualizing but there's nothing playing, idle instead
        v.terminate()
        currently_visualizing = False
        v = Popen(["python", "lavalamp.py"])
        print("idling")

    if (
        not currently_visualizing and rms != 0
    ):  # If we're idling but there's audio playing, visualize it.
        v.terminate()
        currently_visualizing = True
        v = Popen(["python", "blinkpulse.py"])
        print("visualizing")
