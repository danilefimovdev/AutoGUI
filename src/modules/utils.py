import json
import os
import signal
from time import time
from typing import NoReturn

import pygetwindow
import win32con
import win32gui
from win32api import GetKeyboardLayout, GetKeyState

from config import ROOT_DIR


def get_vk(key) -> int:
    """ Get the virtual key code from a key. """

    return key.vk if hasattr(key, 'vk') else key.value.vk


def get_timestamp(start_timer: float) -> float:
    """ get time value passed since start listening process for replaying actions """

    return round(time()-start_timer, ndigits=2)


def get_active_window_title() -> str:
    """ get active window title  """

    try:
        window_title = pygetwindow.getActiveWindowTitle()
        return window_title
    except Exception as ex:
        raise ex


def activate_window(title: str) -> NoReturn:
    """ activate window with passed window title if exists """

    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)
        win32gui.SetForegroundWindow(hwnd)
    else:
        raise Exception(f"There is no window with '{title}' title")


def make_window_switching_record(active_window_title: str, START_TIMER: float) -> NoReturn:
    """ check has the active window changed and make a record of window switching to json """

    make_acting_record(
        controller='window',
        timestamp=get_timestamp(START_TIMER),
        action="switch",
        config=dict(
            title=active_window_title
        )
    )


def make_acting_record(controller: str, timestamp: float, action: str, config: dict) -> NoReturn:
    """ make a record of action to json """

    with open(f'{ROOT_DIR}/records/input_file.json', mode='a') as file:
        data = dict(
            controller=controller,
            timestamp=timestamp,
            action=action,
            config=config
        )
        json.dump(data, file)
        file.write('\n')


def check_is_window_changed(active_window_title: str, START_TIMER: float) -> NoReturn:
    """ check was active window changed and make an action record if It was """

    # get last window name from active_window_name.json file
    with open(f'{ROOT_DIR}/involved_in_recording/active_window_name.json', 'r') as file:
        last_window_title = json.load(file)['title']

    # check is current name different from last_window_title and not equal ("Task Switching", "", "None")
    if active_window_title != last_window_title and active_window_title not in ("Task Switching", "", "None"):

        # change last window name
        with open(f'{ROOT_DIR}/involved_in_recording/active_window_name.json', 'w') as file:
            json.dump(dict(title=active_window_title), file)

        # check was one of window switch hotkey pressed
        with open(f'{ROOT_DIR}/involved_in_recording/switch_window_hotkey.json', 'r') as file:
            is_pressed = json.load(file)['is_pressed']
            if is_pressed:
                # make switch window record
                make_window_switching_record(active_window_title, START_TIMER)

        # change window switch hotkey pressed to false
        with open(f'{ROOT_DIR}/involved_in_recording/switch_window_hotkey.json', 'w') as file:
            json.dump(dict(is_pressed=False), file)


def get_keyboard_language() -> int:
    """ Gets the keyboard language in use by the current active window process. """

    # Get the keyboard layout id
    layout_id = GetKeyboardLayout()

    # Extract the keyboard language id from the keyboard layout id
    language_id = layout_id & (2 ** 16 - 1)

    return language_id


def _clean_temporary_files() -> NoReturn:
    """ clean temporary files using in recording """

    with open(f'{ROOT_DIR}/records/input_file.json', 'w'):
        pass
    with open(f'{ROOT_DIR}/involved_in_recording/active_window_name.json', 'w') as file:
        json.dump(dict(title=get_active_window_title()), file)
    with open(f'{ROOT_DIR}/involved_in_recording/switch_window_hotkey.json', 'w') as file:
        json.dump(dict(is_pressed=False), file)


def _write_capslock_state(START_TIMER: float) -> NoReturn:
    """ write was capslock toggled at the start of the recording """

    caps_lock_vk = 20
    is_caps_lock_toggled = GetKeyState(caps_lock_vk)

    # check if caps lock was toggled at the beginning and make a record of it if It was
    make_acting_record(
        controller='special',
        timestamp=get_timestamp(START_TIMER),
        action="toggle_caps_lock",
        config=dict(subject="capslock", is_toggled=is_caps_lock_toggled)
    )


def _write_start_language(START_TIMER: float) -> NoReturn:
    """ write was capslock toggled at the start of the recording """

    make_acting_record(
        controller='special',
        timestamp=get_timestamp(START_TIMER),
        action="check_language",
        config=dict(subject="language", lang_id=get_keyboard_language())
    )


def _write_start_window(START_TIMER: float) -> NoReturn:
    """ write active window at the start of the recording """

    make_acting_record(
        controller='window',
        timestamp=get_timestamp(START_TIMER),
        action="switch",
        config=dict(title=get_active_window_title())
    )


def do_preparation_actions(START_TIMER: float) -> NoReturn:
    """ do all required actions before starting a new record """

    _clean_temporary_files()
    _write_capslock_state(START_TIMER)
    _write_start_language(START_TIMER)
    _write_start_window(START_TIMER)


def stop_process() -> NoReturn:
    """Catch expected hotkey and terminate started process"""

    print(f'Stop listening')
    os.kill(os.getpid(), signal.SIGTERM)
