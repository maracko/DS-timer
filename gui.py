# !/usr/bin/env python
import PySimpleGUIQt as sg
import keyboard as kb
from time import time, sleep
from typing import Dict
from pathlib import Path
from playsound import playsound
import json
import base64
from webbrowser import open as web_open
from threading import Timer

SETTINGS_FILE = Path(__file__).parent / "settings.cfg"
ICON_FILE = Path(__file__).parent / "resources" / "DS.ico"
ICON = str(ICON_FILE)

##Base64 version of icon for the tray
icon = ICON_FILE.read_bytes()
base64_icon = base64.b64encode(icon)


DEFAULT_SETTINGS = {
    "start_timer_sound": str(Path(__file__).parent / "resources" / "Start.wav"),
    "start_timer_1": "ctrl+shift+1",
    "start_timer_2": "ctrl+shift+2",
    "start_timer_3": "ctrl+shift+3",
    "start_timer_4": "ctrl+shift+4",
    "stop_timer_1": "ctrl+alt+1",
    "stop_timer_2": "ctrl+alt+2",
    "stop_timer_3": "ctrl+alt+3",
    "stop_timer_4": "ctrl+alt+4",
    "timer_sound_1": str(Path(__file__).parent / "resources" / "Finish_1.mp3"),
    "timer_sound_2": str(Path(__file__).parent / "resources" / "Finish_2.mp3"),
    "timer_sound_3": str(Path(__file__).parent / "resources" / "Finish_3.mp3"),
    "timer_sound_4": str(Path(__file__).parent / "resources" / "Finish_4.mp3"),
    "stop_timer_sound_1": str(Path(__file__).parent / "resources" / "Cancel_1.mp3"),
    "stop_timer_sound_2": str(Path(__file__).parent / "resources" / "Cancel_2.mp3"),
    "stop_timer_sound_3": str(Path(__file__).parent / "resources" / "Cancel_3.mp3"),
    "stop_timer_sound_4": str(Path(__file__).parent / "resources" / "Cancel_4.mp3"),
    "theme": "DarkAmber",
    "timeout": 1,
}

SETTINGS_KEYS_TO_ELEMENT_KEYS = {
    "start_timer_sound": "-START SOUND-",
    "start_timer_1": "-TIMER 1-",
    "start_timer_2": "-TIMER 2-",
    "start_timer_3": "-TIMER 3-",
    "start_timer_4": "-TIMER 4-",
    "stop_timer_1": "-STOP 1-",
    "stop_timer_2": "-STOP 2-",
    "stop_timer_3": "-STOP 3-",
    "stop_timer_4": "-STOP 4-",
    "timer_sound_1": "-SOUND 1-",
    "timer_sound_2": "-SOUND 2-",
    "timer_sound_3": "-SOUND 3-",
    "timer_sound_4": "-SOUND 4-",
    "stop_timer_sound_1": "-STOP SOUND 1-",
    "stop_timer_sound_2": "-STOP SOUND 2-",
    "stop_timer_sound_3": "-STOP SOUND 3-",
    "stop_timer_sound_4": "-STOP SOUND 4-",
    "theme": "-THEME-",
    "timeout": "-TIMEOUT-",
}

# Load settings from json file
def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
    except Exception as e:
        sg.popup_error(
            f"No settings file found... will create one for you",
            keep_on_top=True,
            background_color="yellow",
            text_color="black",
        )
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


# Save settings to json file
def save_settings(settings_file, settings, values):
    if values:  # if there are stuff specified by another window, fill in those values
        for (
            key
        ) in (
            SETTINGS_KEYS_TO_ELEMENT_KEYS
        ):  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f"Problem updating settings from window values. Key = {key}")

    with open(settings_file, "w") as f:
        json.dump(settings, f)

    sg.popup("Settings saved")


def create_settings_window(settings):
    sg.theme(settings["theme"])

    def TextLabel(text):
        return sg.Text(text + ":", justification="r", size=(15, 1))

    layout = [
        [sg.Text("Settings", font="Any 15", justification="center")],
        [TextLabel("Start timer 1 hotkey"), sg.Input(key="-TIMER 1-")],
        [TextLabel("Start timer 2 hotkey"), sg.Input(key="-TIMER 2-")],
        [TextLabel("Start timer 3 hotkey"), sg.Input(key="-TIMER 3-")],
        [TextLabel("Start timer 4 hotkey"), sg.Input(key="-TIMER 4-")],
        [TextLabel("Stop timer 1 hotkey"), sg.Input(key="-STOP 1-")],
        [TextLabel("Stop timer 2 hotkey"), sg.Input(key="-STOP 2-")],
        [TextLabel("Stop timer 3 hotkey"), sg.Input(key="-STOP 3-")],
        [TextLabel("Stop timer 4 hotkey"), sg.Input(key="-STOP 4-")],
        [
            TextLabel("Start timer sound"),
            sg.Input(key="-START SOUND-"),
            sg.FileBrowse(target="-START SOUND-"),
        ],
        [
            TextLabel("Timer 1 finished"),
            sg.Input(key="-SOUND 1-"),
            sg.FileBrowse(target="-SOUND 1-"),
        ],
        [
            TextLabel("Timer 2 finished"),
            sg.Input(key="-SOUND 2-"),
            sg.FileBrowse(target="-SOUND 2-"),
        ],
        [
            TextLabel("Timer 3 finished"),
            sg.Input(key="-SOUND 3-"),
            sg.FileBrowse(target="-SOUND 3-"),
        ],
        [
            TextLabel("Timer 4 finished"),
            sg.Input(key="-SOUND 4-"),
            sg.FileBrowse(target="-SOUND 4-"),
        ],
        [
            TextLabel("Timer 1 canceled"),
            sg.Input(key="-STOP SOUND 1-"),
            sg.FileBrowse(target="-STOP SOUND 1-"),
        ],
        [
            TextLabel("Timer 2 canceled"),
            sg.Input(key="-STOP SOUND 2-"),
            sg.FileBrowse(target="-STOP SOUND 2-"),
        ],
        [
            TextLabel("Timer 3 canceled"),
            sg.Input(key="-STOP SOUND 3-"),
            sg.FileBrowse(target="-STOP SOUND 3-"),
        ],
        [
            TextLabel("Timer 4 canceled"),
            sg.Input(key="-STOP SOUND 4-"),
            sg.FileBrowse(target="-STOP SOUND 4-"),
        ],
        [
            sg.Text("Timeout between keypresses (seconds)", justification="r"),
            sg.Input(key="-TIMEOUT-"),
        ],
        [sg.Text("Theme"), sg.Combo(sg.theme_list(), key="-THEME-")],
        [sg.Button("Save"), sg.Button("Exit")],
    ]

    window = sg.Window("Settings", layout, keep_on_top=True, finalize=True, icon=ICON)

    for (
        key
    ) in (
        SETTINGS_KEYS_TO_ELEMENT_KEYS
    ):  # update window with the values read from settings file
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f"Problem updating PySimpleGUI window from settings. Key = {key}")

    return window


def create_main_window(settings):
    sg.theme(settings["theme"])

    layout = [
        [
            sg.Menu(
                [["&File", ["&Exit"]], ["&Edit", ["&Settings"]], ["&Help", ["&About"]]]
            )
        ],
        [sg.Text("Welcome to DS timer!")],
        [
            sg.Button(
                "Start 1", key="-BUTTON 1-", enable_events=True, change_submits=True
            ),
            sg.Button("Start 2", key="-BUTTON 2-"),
            sg.Button("Start 3", key="-BUTTON 3-"),
            sg.Button("Start 4", key="-BUTTON 4-"),
        ],
        [sg.Text("Info about your timers: ")],
        [sg.Output()],
        [sg.Button("Minimize to tray"), sg.Exit()],
    ]

    return sg.Window(
        "DS timer",
        layout,
        return_keyboard_events=True,
        use_default_focus=False,
        icon=ICON,
    )


def create_system_tray():
    menu = [
        "DS timer",
        [
            "&Restore",
            "&Settings",
            "&Exit",
        ],
    ]
    tray = sg.SystemTray(menu=menu, data_base64=base64_icon, tooltip="DS timer")
    tray.Hide()

    return tray


def create_about_window(settings):
    sg.theme(settings["theme"])

    layout = [
        [sg.Text("About", font="Any 15", justification="center")],
        [
            sg.Text(
                "Simple application to track survivor DS time and avoid getting hit by it at 59.9s :)",
                justification="center",
                auto_size_text=True,
            )
        ],
        [
            sg.Text(
                "Built with python using keyboard module and PySimpleGUIQt",
                justification="center",
                auto_size_text=True,
            )
        ],
        [
            sg.Text(
                "Made by Mario Petričko",
                justification="center",
                auto_size_text=True,
            )
        ],
        [
            sg.Text(
                "www.github.com/maracko",
                justification="center",
                auto_size_text=True,
                enable_events=True,
                key="-GITHUB LINK-",
            )
        ],
        [sg.Button("Ok")],
    ]

    window = sg.Window("About", layout, icon=ICON)
    return window


last_pressed_dict = {}
timers: Dict[int, Timer] = {}
button_timer_map = ["-BUTTON 1-", "-BUTTON 2-", "-BUTTON 3-", "-BUTTON 4-"]


def handle_start_hotkey(window: sg.Window, number: int, hotkey: str, settings: dict):
    # check if last pressed time is more than current time minus the timeout value
    # this is to avoid rapidly printing to output window, basically rate limiting
    if time() - last_pressed_dict.get(hotkey, 0) >= int(settings["timeout"]):
        # set the last pressed time to now
        last_pressed_dict[hotkey] = time()
        # if timer exists
        if number in timers:
            # if it is not running create it again
            if not timers[number].is_alive():
                print(f"Timer {number} started")
                playsound(settings["start_timer_sound"], block=False)
                timers[str(number)] = Timer(
                    60, print, [f"Timer {number} finished", False]
                )
                timers[number] = Timer(
                    60, playsound, [settings[f"timer_sound_{number}"], False]
                )
                timers[number].start()
                timers[str(number)].start()
                window[button_timer_map[number - 1]].Update(f"Stop {number}")
        else:
            # if it doesn't exist create one
            print(f"Timer {number} started")
            playsound(settings["start_timer_sound"], block=False)
            timers[str(number)] = Timer(60, print, [f"Timer {number} finished", False])
            timers[number] = Timer(60, playsound, [settings[f"timer_sound_{number}"]])
            timers[number].start()
            timers[str(number)].start()
            window[button_timer_map[number - 1]].Update(f"Stop {number}")


def handle_stop_hotkey(window: sg.Window, number: int, hotkey: str, settings: dict):
    if time() - last_pressed_dict.get(hotkey, 0) >= int(settings["timeout"]):
        last_pressed_dict[hotkey] = time()
        if number in timers:
            if timers[number].is_alive():
                print(f"Canceled timer {number}..")
                playsound(settings[f"stop_timer_sound_{number}"], block=False)
                timers[number].cancel()
                window[button_timer_map[number - 1]].Update(f"Start {number}")
        if str(number) in timers:
            if timers[str(number)].is_alive():
                timers[str(number)].cancel()


def handle_timer_button(window: sg.Window, button: str, settings: dict):
    if button in button_timer_map:
        ##Get the timer number based on button pressed
        number = button_timer_map.index(button) + 1
    if number in timers:
        if timers[number].is_alive():
            playsound(settings[f"stop_timer_sound_{number}"], block=False)
            timers[number].cancel()
            print(f"Canceled timer {number}..")
            window[button].Update(f"Start {number}")
        else:
            print(f"Timer {number} started")
            playsound(settings["start_timer_sound"], block=False)
            # Start thread for printing of when timer is done, using string instead of int for it's key
            timers[str(number)] = Timer(60, print, [f"Timer {number} finished", False])
            # Start thread for timer sound
            timers[number] = Timer(
                60, playsound, [settings[f"timer_sound_{number}"], False]
            )
            timers[number].start()
            window[button].Update(f"Stop {number}")

    else:
        # if it doesn't exist create one
        print(f"Timer {number} started")
        playsound(settings["start_timer_sound"], block=False)
        timers[str(number)] = Timer(60, print, [f"Timer {number} finished", False])
        timers[number] = Timer(60, playsound, [settings[f"timer_sound_{number}"]])
        timers[number].start()
        window[button].Update(f"Stop {number}")


def stop_all_timers(timers: dict, window: sg.Window, buttons):
    try:
        for timer in timers.values():
            timer.cancel()
    except Exception:
        pass
    for i, button in enumerate(buttons):
        window[button].Update(f"Start {i+1}")


def main():
    tray_visible = False
    window_visible = True
    tray = create_system_tray()
    window = None
    settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS)
    while True:  # Event Loop
        if window_visible:
            try:
                sleep(0.01)
                if window is None:
                    window = create_main_window(settings)
                event, values = window.read(timeout=0)
                if event in (sg.WIN_CLOSED, "Exit"):
                    # Stopping all timers and exiting app
                    stop_all_timers(timers, window, button_timer_map)
                    break
                elif event == "Minimize to tray":
                    window.hide()
                    tray.UnHide()
                    tray_visible = True
                    window_visible = False
                if event == "Settings":
                    stop_all_timers(timers, window, button_timer_map)
                    event, values = create_settings_window(settings).read(close=True)
                    if event == "Save":
                        window.close()
                        window = None
                        save_settings(SETTINGS_FILE, settings, values)
                elif event == "About":
                    event, values = create_about_window(settings).read(close=True)
                    if event == "-GITHUB LINK-":
                        web_open("www.github.com/maracko")
                    elif event == "Ok":
                        window.close()
                        window = None
                ## HANDLING TIMER BUTTONS ##
                elif (
                    event == "-BUTTON 1-"
                    or event == "-BUTTON 2-"
                    or event == "-BUTTON 3-"
                    or event == "-BUTTON 4-"
                ):
                    handle_timer_button(window, event, settings)
                ## TODO tidy up hotkey events, maybe extract to a function ##
                ## HANDLING START HOTKEYS ##
                if kb.is_pressed(settings["start_timer_1"]):
                    handle_start_hotkey(window, 1, settings["start_timer_1"], settings)
                elif kb.is_pressed(settings["start_timer_2"]):
                    handle_start_hotkey(window, 2, settings["start_timer_2"], settings)
                elif kb.is_pressed(settings["start_timer_3"]):
                    handle_start_hotkey(window, 3, settings["start_timer_3"], settings)
                elif kb.is_pressed(settings["start_timer_4"]):
                    handle_start_hotkey(window, 4, settings["start_timer_4"], settings)

                ## HANDLING STOP HOTKEYS ##
                elif kb.is_pressed(settings["stop_timer_1"]):
                    handle_stop_hotkey(window, 1, settings["stop_timer_1"], settings)
                elif kb.is_pressed(settings["stop_timer_2"]):
                    handle_stop_hotkey(window, 2, settings["stop_timer_1"], settings)
                elif kb.is_pressed(settings["stop_timer_3"]):
                    handle_stop_hotkey(window, 3, settings["stop_timer_1"], settings)
                elif kb.is_pressed(settings["stop_timer_4"]):
                    handle_stop_hotkey(window, 4, settings["stop_timer_1"], settings)
            except Exception as e:
                print(f"Error : {e}, {e.args}")
        elif tray_visible:
            sleep(0.01)
            event, values = window.read(timeout=0)
            menu_item = tray.read(timeout=0)
            if (
                menu_item == "Restore"
                or menu_item == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED
            ):
                tray.hide()
                tray_visible = False
                window_visible = True
                window.UnHide()
            elif menu_item == "Settings":
                event, values = create_settings_window(settings).read(close=True)
                if menu_item == "Save":
                    window.close()
                    window = None
                    save_settings(SETTINGS_FILE, settings, values)
            if kb.is_pressed(settings["start_timer_1"]):
                handle_start_hotkey(window, 1, settings["start_timer_1"], settings)
            elif kb.is_pressed(settings["start_timer_2"]):
                handle_start_hotkey(window, 2, settings["start_timer_2"], settings)
            elif kb.is_pressed(settings["start_timer_3"]):
                handle_start_hotkey(window, 3, settings["start_timer_3"], settings)
            elif kb.is_pressed(settings["start_timer_4"]):
                handle_start_hotkey(window, 4, settings["start_timer_4"], settings)

            ## HANDLING STOP HOTKEYS ##
            elif kb.is_pressed(settings["stop_timer_1"]):
                handle_stop_hotkey(window, 1, settings["stop_timer_1"], settings)
            elif kb.is_pressed(settings["stop_timer_2"]):
                handle_stop_hotkey(window, 2, settings["stop_timer_1"], settings)
            elif kb.is_pressed(settings["stop_timer_3"]):
                handle_stop_hotkey(window, 3, settings["stop_timer_1"], settings)
            elif kb.is_pressed(settings["stop_timer_4"]):
                handle_stop_hotkey(window, 4, settings["stop_timer_1"], settings)
            elif menu_item == "Exit":
                break
    window.close()


if __name__ == "__main__":
    main()