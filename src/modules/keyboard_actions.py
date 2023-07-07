from typing import NoReturn

from pynput.keyboard import KeyCode, Controller
from win32api import GetKeyState

from src.modules.utils import get_active_window_title, check_is_window_changed, make_acting_record, get_timestamp, \
    get_vk


# ------ keyboard listening functions ------ #


def on_press(key, START_TIMER: float) -> NoReturn:
    """catch keyboard's key pressing and write in the log file"""

    # check has the window changed from last action and make record if True
    active_window_title = get_active_window_title()
    check_is_window_changed(active_window_title, START_TIMER)

    # make record of action
    make_acting_record(
        controller="keyboard",
        timestamp=get_timestamp(START_TIMER),
        action="press",
        config=dict(key=get_vk(key))
    )


def on_release(key, START_TIMER: float) -> NoReturn:
    """catch keyboard's key releasing and write in the log file"""

    # check has the window changed from last action and make record if True
    active_window_title = get_active_window_title()
    check_is_window_changed(active_window_title, START_TIMER)

    # make record of action
    make_acting_record(
        controller="keyboard",
        timestamp=get_timestamp(START_TIMER),
        action="release",
        config=dict(key=get_vk(key))
    )


# ------ keyboard playing functions ------ #


def press_keyboard(config: dict, controller: Controller) -> NoReturn:
    """ press keyboard key """

    key_code = KeyCode.from_vk(config['key'])
    controller.press(key_code)


def release_keyboard(config: dict, controller: Controller) -> NoReturn:
    """ release keyboard key """

    key_code = KeyCode.from_vk(config['key'])
    controller.release(key_code)


def toggle_capslock(config: dict, controller: Controller) -> NoReturn:

    caps_lock_vk = 20
    is_caps_lock_toggled = GetKeyState(caps_lock_vk)
    if is_caps_lock_toggled != config['is_toggled']:
        key_code = KeyCode.from_vk(caps_lock_vk)
        controller.press(key_code)
        controller.release(key_code)
