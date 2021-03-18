##Now obsolete CLI that was used as a POC using AHK and keyboard
from ahk import AHK, Hotkey
from pathlib import Path
from time import sleep
from termcolor import cprint
import sys
import keyboard
import argparse

# import logging
# logging.basicConfig(level=logging.DEBUG)

# Adding and parsing args
parser = argparse.ArgumentParser()

parser.add_argument(
    "--hotkey",
    "--h",
    default="ctrl,shift,q",
    help="Key combo to start the timer.Please use ',' to separate keys. Default = ctrl,shift,q",
)
parser.add_argument(
    "--stop",
    "--s",
    default="ctrl+shift+1",
    help="Key combo to stop the timer.Please use ',' to separate keys. Default = ctrl,shift,1",
)

parser.add_argument(
    "--time",
    "--t",
    default=60000,
    type=int,
    help="Timer length in milliseconds. Default = 60000 (1min)",
)

parser.add_argument(
    "--audio",
    "--a",
    default=Path(__file__).parent.joinpath("timeisUp.wav"),
    type=str,
    help=r"Enter full path to audio file for timer, default is currentFolder\timeIsUp.wav",
)

args = parser.parse_args()

# Dict of ahk syntax modifiers to replace arguments for timer start
hotkey_dict = {"ctrl": "^", "shift": "+", "win": "#", "alt": "!", ",": ""}
hotkey: str = args.hotkey
hotkey = hotkey.lower()
restart: str = hotkey.replace(",", "+")
# Parsing hotkey
for original, modified in hotkey_dict.items():
    hotkey = hotkey.replace(original, modified)

# Keyboard module which is used to stop the timer has a different syntax from ahk
stop: str = args.stop.replace(",", "+")
time: int = args.time
audio: str = args.audio

ahk = AHK()

script = f"""
;<- is for comments
Timer:
SoundPlay *-1
Sleep, {time}
SoundPlay, {audio}
"""  # Define an ahk script
macro = Hotkey(ahk, hotkey, script)  # Create Hotkey
macro.start()  #  Start listening for hotkey

cprint("Application started...", "blue", "on_grey")
cprint("You will hear an alert sound on timer activation", "blue", "on_grey")
try:
    while True:
        if keyboard.is_pressed(stop) and macro.running:
            cprint(
                "Stopped listening for hotkey and aborted any active timers",
                "yellow",
                "on_grey",
            )
            macro.stop()
            continue
        elif keyboard.is_pressed(restart) and not macro.running:
            try:
                cprint("Listening for hotkey again", "green", "on_grey")
                macro.start()
            except Exception as e:
                cprint("Error has occured: {}".format(e.args), "red", "on_grey")
        sleep(0.05)
except KeyboardInterrupt:
    cprint("Exiting...", "red", "on_grey")
    sys.exit(0)