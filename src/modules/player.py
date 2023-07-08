import json
import sys
from time import time, sleep
from typing import NoReturn

import keyboard
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, KeyCode
from win32api import GetKeyState

from utils import activate_window, get_timestamp, stop_process, ask_user_for_a_record_name, get_keyboard_language
from defaullts import ROOT_DIR, MOUSE_BUTTONS, LANGUAGES

# ------ start time counter ------ #


START_TIMER = time()


# ------ mouse actions ------ #


MOUSE = MouseController()


def move_to(config: dict) -> NoReturn:
    """ change mouse position """

    MOUSE.position = (config['x'], config['y'])


def press_mouse(config: dict) -> NoReturn:
    """ press mouse button """

    if MOUSE.position != (config['x'], config['y']):
        move_to(config)
    MOUSE.press(MOUSE_BUTTONS[config['button']])


def release_mouse(config: dict) -> NoReturn:
    """ release mouse button """

    if MOUSE.position != (config['x'], config['y']):
        move_to(config)
    MOUSE.release(MOUSE_BUTTONS[config['button']])


def scroll_mouse(config: dict) -> NoReturn:
    """ do mouse scroll """

    if MOUSE.position != (config['x'], config['y']):
        move_to(config)
    dx = 0
    MOUSE.scroll(dx, config['dy'])


MOUSE_ACTIONS = {
    'scroll': scroll_mouse,
    'press': press_mouse,
    'release': release_mouse,
    'move': move_to
}


# ------ keyboard actions ------ #


KEYBOARD = KeyboardController()


def press_keyboard(config: dict) -> NoReturn:
    """ press keyboard key """

    key_code = KeyCode.from_vk(config['key'])
    KEYBOARD.press(key_code)


def release_keyboard(config: dict) -> NoReturn:
    """ release keyboard key """

    key_code = KeyCode.from_vk(config['key'])
    KEYBOARD.release(key_code)


def toggle_capslock(config: dict) -> NoReturn:

    caps_lock_vk = 20
    is_caps_lock_toggled = GetKeyState(caps_lock_vk)
    if is_caps_lock_toggled != config['is_toggled']:
        key_code = KeyCode.from_vk(caps_lock_vk)
        KEYBOARD.press(key_code)
        KEYBOARD.release(key_code)


KEYBOARD_ACTIONS = {
    'press': press_keyboard,
    'release': release_keyboard,
    'toggle_capslock': toggle_capslock,
}


# ------ special actions ------ #


def switch_window(config: dict) -> NoReturn:
    """ switch to the window with passed title if the window exists """

    try:
        activate_window(config['title'])
    except Exception as ex:
        raise ex


def check_language(config: dict) -> NoReturn:

    current_lang = get_keyboard_language()
    lang_name = LANGUAGES[config['lang_id']]
    if current_lang != config['lang_id']:
        raise Exception(f'Wrong keyboard layout. Change it to "{lang_name}"')


SPECIAL_ACTIONS = {
    'check_language': check_language,
    'activate_window': activate_window
}


# ------ main function ------ #


# TODO: think how we can pass the length of stop recording hotkey dynamically
# TODO: or find out how we can remove records of pressing stop record hotkey from the end
def main():

    # set terminate playing hotkeys
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/config.json', mode='r') as file:
        config = json.load(file)

        hotkeys = config["STOP_PLAYING_HOTKEYS"]
        for hotkey in hotkeys:
            keyboard.add_hotkey(hotkey, stop_process)

        # the number of actions recorded as a result of pressing the stop recording hotkey (we do not need to play them)
        acts_to_ignore = hotkeys[0].count("+")
        # pause between timestamp check
        pause = config["TIMESTAMP_CHECK_PAUSE"]


    # ask user for record file name to start
    file_name = ask_user_for_a_record_name()

    try:
        with open(f'{ROOT_DIR}/records/{file_name}', mode='r') as file:
            error_timestamp = None

            limit = (len(file.readlines()) - acts_to_ignore)
            file.seek(0)  # move reading cursor to the beginning of the file
            for line in file.readlines()[0:limit]:
                item = json.loads(line)

                # here we are waiting when action time would be equal or less than start script time
                while item['timestamp'] > get_timestamp(START_TIMER):
                    sleep(pause)
                error_timestamp = item['timestamp']
                # when the time is right we start the action
                if item['controller'] == 'mouse':
                    MOUSE_ACTIONS[item['action']](item['config'])
                elif item['controller'] == 'keyboard':
                    KEYBOARD_ACTIONS[item['action']](item['config'])
                else:  # special (language change, window switch)
                    SPECIAL_ACTIONS[item['action']](item['config'])
            print(f'Finished playing {file_name}')
    except Exception as ex:
        print(f"Timestamp: {error_timestamp} s. - Error: {ex} - File: {file_name}")
    finally:
        sys.exit()


# ------ execution point ------ #


if __name__ == '__main__':
    main()


