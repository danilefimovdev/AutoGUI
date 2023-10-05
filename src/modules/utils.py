import ctypes
import json
import os
import signal
from datetime import datetime
from time import time
from typing import Optional

import keyboard
import win32con
import win32gui
from win32api import GetKeyboardLayout, GetKeyState

from defaullts import ROOT_DIR


START_TIMER = time()


def get_vk(key) -> int:
    """ Get the virtual key code from a key. """

    return key.vk if hasattr(key, 'vk') else key.value.vk


def get_timestamp() -> float:
    """ get time value passed since start listening process for replaying actions """

    return round(time()-START_TIMER, ndigits=2)


def get_active_window_title() -> Optional[str]:
    """ get active window title  """

    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return title
    except Exception as ex:
        raise ex
        # return None


def activate_window(config: dict) -> None:
    """ activate window with passed window title if exists """

    title = config["title"]
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)
        win32gui.SetForegroundWindow(hwnd)
    else:
        raise Exception(f"There is no window with '{title}' as title")


def make_window_switching_record(active_window_title: str) -> None:
    """ check has the active window changed and make a record of window switching to json """

    try:
        make_acting_record(
            controller='special',
            action="activate_window",
            config=dict(
                title=active_window_title
            )
        )
    except Exception as ex:
        raise ex


def make_acting_record(controller: str, action: str, config: dict) -> None:
    """ make a record of action to json """

    try:
        with open(f'{ROOT_DIR}/records/input_file.json', mode='a') as file:
            data = dict(
                controller=controller,
                timestamp=get_timestamp(),
                action=action,
                config=config
            )
            json.dump(data, file)
            file.write('\n')
    except Exception as ex:
        raise ex


def check_is_window_changed(active_window_title: str) -> None:
    """ check was active window changed and make an action record if It was """

    # get last window name from active_window_name.txt file
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/active_window_name.txt', 'r') as file:
        last_window_title = file.readline()

    with open(f'{ROOT_DIR}/used_in_recording_&_playing/switch_window_name.txt', 'r') as file:
        switch_window_title = file.readline()

    # check is current name different from last_window_title and not equal ("Task Switching", "", "None")
    if active_window_title not in ("Task Switching", "", "None", "Task View") and active_window_title is not None:

        # change last window name
        try:
            with open(f'{ROOT_DIR}/used_in_recording_&_playing/active_window_name.txt', 'w', encoding="utf-8") as file:
                file.write(active_window_title)
        except Exception as ex:
            raise ex

        with open(f'{ROOT_DIR}/used_in_recording_&_playing/switch_window_hotkey.txt', 'r') as file:
            try:
                is_pressed = int(file.read())
            except ValueError:
                is_pressed = None

        # print(f"active_window != last_window: {active_window_title != last_window_title}; is_pressed: {is_pressed}; active_window: {active_window_title}; last_window: {last_window_title};")
        # print(f"active_window == switch_window: {active_window_title == switch_window_title}; is_pressed: {is_pressed}; active_window: {active_window_title}; switch_window: {switch_window_title};")

        first_condition = active_window_title != last_window_title
        second_condition = all((active_window_title == switch_window_title, is_pressed,))
        if is_pressed is not None:
            if first_condition or second_condition:
                try:
                    # check was one of window switch hotkey pressed
                    if is_pressed:
                        # make switch window record
                        make_window_switching_record(active_window_title)

                        if second_condition:
                            switch_window = ""
                        else:  # first_condition
                            switch_window = active_window_title
                        with open(f'{ROOT_DIR}/used_in_recording_&_playing/switch_window_name.txt', 'w', encoding="utf-8") as file:
                            file.write(switch_window)

                    # change window switch hotkey pressed to false
                    with open(f'{ROOT_DIR}/used_in_recording_&_playing/switch_window_hotkey.txt', 'w') as file:
                        file.write("0")
                except Exception as ex:
                    raise ex


def get_keyboard_language() -> int:
    """ Gets the keyboard language in use by the current active window process. """

    # Get the keyboard layout id
    layout_id = GetKeyboardLayout()

    # Extract the keyboard language id from the keyboard layout id
    language_id = layout_id & (2 ** 16 - 1)

    return language_id


def stop_process() -> None:
    """Catch expected hotkey and terminate started process"""

    os.kill(os.getpid(), signal.SIGTERM)
    print(f'Stop listening')


def ask_user_for_a_record_name() -> str:

    file_name = None
    while not file_name:
        entered_data = input('Enter json file name with .json: ')
        if os.path.exists(f"{ROOT_DIR}/records/{entered_data.replace(' ', '')}"):
            file_name = entered_data
        else:
            print(f'0 records with "{entered_data}" name were found')
            print(f'Please enter valid file name')
    return file_name


def _clean_temporary_files() -> None:
    """ clean temporary files using in recording """

    with open(f'{ROOT_DIR}/records/input_file.json', 'w'):
        pass
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/active_window_name.txt', 'w') as file:
        file.write(get_active_window_title())
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/switch_window_hotkey.txt', 'w') as file:
        file.write("0")
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/switch_window_name.txt', 'w') as file:
        file.write("")


def _write_capslock_state() -> None:
    """ write was capslock toggled at the start of the recording """

    caps_lock_vk = 20
    is_capslock_toggled = GetKeyState(caps_lock_vk)

    # check if caps lock was toggled at the beginning and make a record of it if It was
    make_acting_record(
        controller="keyboard",
        action="toggle_capslock",
        config=dict(is_toggled=is_capslock_toggled)
    )


def _write_start_language() -> None:
    """ write was capslock toggled at the start of the recording """

    make_acting_record(
        controller='special',
        action="check_language",
        config=dict(subject="language", lang_id=get_keyboard_language())
    )


def _write_start_window_as_action() -> None:
    """ write active window at the start of the recording """

    make_acting_record(
        controller="special",
        action="activate_window",
        config=dict(title=get_active_window_title())
    )


def _write_opened_at_start_windows() -> None:
    """ write set of opened windows at the start of recording"""

    with open(f'{ROOT_DIR}/used_in_recording_&_playing/open_windows_at_start.json', 'w', encoding='utf-8') as file:
        windows = get_open_windows()
        data = {"windows": list(windows)}
        json.dump(data, file)


def do_preparation_actions() -> None:
    """ do all required actions before starting a new record """

    _clean_temporary_files()
    _write_capslock_state()
    _write_start_language()
    _write_start_window_as_action()
    _write_opened_at_start_windows()


def set_hotkeys(window_switch: bool = False, stop_recording: bool = False, stop_playing: bool = False):
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/config.json', mode='r') as file:
        config = json.load(file)
        if window_switch:
            switch_hotkeys = config["SWITCH_WINDOW_HOTKEYS"]
            for hotkey in switch_hotkeys:  # set window switched flag hotkeys
                keyboard.add_hotkey(hotkey, write_window_switch)
        if stop_recording:
            stop_hotkeys = config["STOP_RECORDING_HOTKEYS"]
            for hotkey in stop_hotkeys:  # set window switched flag hotkeys
                keyboard.add_hotkey(hotkey, stop_process)
        if stop_playing:
            stop_hotkeys = config["STOP_PLAYING_HOTKEYS"]
            for hotkey in stop_hotkeys:  # set window switched flag hotkeys
                keyboard.add_hotkey(hotkey, stop_process)


def write_window_switch() -> None:

    with open(f'{ROOT_DIR}/used_in_recording_&_playing/switch_window_hotkey.txt', 'w') as file:
        file.write("1")


def get_current_datetime() -> str:
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return current_datetime


def get_open_windows() -> set:
    """get set of all opened windows titles"""

    windows = set()

    def is_visible(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window = win32gui.GetWindowText(hwnd)
            if window:  # here we escape None title windows
                windows.add(window)

    win32gui.EnumWindows(is_visible, None)

    return windows


def get_windows_to_switch_from_log() -> set:

    windows = set()

    with open(f'{ROOT_DIR}/records/input_file.json', 'r') as file:
        for line in file.readlines():
            item = json.loads(line)
            if item['action'] == "activate_window":
                windows.add(item["config"]["title"])

    return windows


def get_required_to_be_opened_at_start_windows() -> list:

    windows_to_switch = get_windows_to_switch_from_log()
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/open_windows_at_start.json', 'r', encoding="utf-8") as file:
        windows_at_start = set(json.loads(file.readline())['windows'])
    required_windows = windows_at_start.intersection(windows_to_switch)
    return list(required_windows)


def write_required_windows_in_log(required_windows: list) -> None:

    with open(f'{ROOT_DIR}/records/input_file.json', 'r+', encoding='utf-8') as file:
        data = file.read()
        file.seek(0)
        config = {'windows': required_windows}
        note = dict(
            controller="special",
            timestamp=0.0,
            action="check_are_required_windows_opened",
            config=config
        )
        str_data = json.dumps(note)

        file.write(f'{str_data}\n' + data )

