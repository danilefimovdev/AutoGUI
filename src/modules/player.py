import json
import os.path
import sys
from time import time, sleep
from typing import NoReturn

import keyboard
import pygetwindow
from win32api import GetKeyState
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, KeyCode

from config import ROOT_DIR, STOP_PLAYING_HOTKEYS
from utils import activate_window, get_timestamp, get_keyboard_language, stop_process
from defaullts import LANGUAGES, MOUSE_BUTTONS

# ------ start time counter ------ #


START_TIMER = time()


# ------ mouse actions ------ #


MOUSE = MouseController()


# TODO: put this part of the code in a separate file


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


KEYBOARD_ACTIONS = {
    'press': press_keyboard,
    'release': release_keyboard
}


# ------ window actions ------ #


def switch_window(config: dict):
    """ switch to the window with passed title if the window exists """

    try:
        activate_window(config['title'])
    except pygetwindow.PyGetWindowException as ex:
        raise ex


# ------ special function ------ #


def check_language(config: dict) -> NoReturn:

    current_lang = get_keyboard_language()
    lang_name = LANGUAGES[config['lang_id']]
    if current_lang != config['lang_id']:
        raise Exception(f'Wrong keyboard layout. Change it to "{lang_name}"')


def toggle_caps_lock(config: dict) -> NoReturn:

    caps_lock_vk = 20
    is_caps_lock_toggled = GetKeyState(caps_lock_vk)
    if is_caps_lock_toggled != config['is_toggled']:
        key_code = KeyCode.from_vk(caps_lock_vk)
        KEYBOARD.press(key_code)
        KEYBOARD.release(key_code)


SPECIAL_ACTIONS = {
    'capslock': toggle_caps_lock,
    'language': check_language
}


# ------ main function ------ #


def main():

    # set terminate playing hotkeys
    for hotkey in STOP_PLAYING_HOTKEYS:
        keyboard.add_hotkey(hotkey, stop_process)

    timestamp_check_pause = 0.01

    # ask user for record file name to start
    file_name = None
    while not file_name:
        entered_data = input('Enter json file name with .json: ')
        if os.path.exists(f"{ROOT_DIR}/records/{entered_data.replace(' ', '')}"):
            file_name = entered_data
        else:
            print(f'0 records with "{entered_data}" name were found')
            print(f'Please enter valid file name')

    try:
        with open(f'{ROOT_DIR}/records/{file_name}', mode='r') as file:
            error_timestamp = None
            # TODO: think how we can pass the length of stop recording hotkey dynamically
            # TODO: or find out how we can remove records of pressing stop record hotkey from the end

            hotkey_keys_numb = 2  # changes depends on hotkey that stops recording
            file_lines_limit = (len(file.readlines()) - hotkey_keys_numb)  # limit that cuts off lines of hotkey pressing
            file.seek(0)  # move reading cursor to the beginning of the file
            for line in file.readlines()[0:file_lines_limit]:
                item = json.loads(line)

                # here we are waiting when action time would be equal or less than start script time
                while item['timestamp'] > get_timestamp(START_TIMER):
                    sleep(timestamp_check_pause)
                error_timestamp = item['timestamp']
                # when the time is right we start the action
                if item['controller'] == 'mouse':
                    MOUSE_ACTIONS[item['action']](item['config'])
                elif item['controller'] == 'keyboard':
                    KEYBOARD_ACTIONS[item['action']](item['config'])
                elif item['controller'] == 'window':
                    switch_window(item['config'])
                else:  # special (caps lock toggle, language change)
                    SPECIAL_ACTIONS[item['config']['subject']](item['config'])
            print(f'Finished playing {file_name}')
    except Exception as ex:
        print(f"Timestamp: {error_timestamp} s. - Error: {ex} - File: {file_name}")
    finally:
        sys.exit()

# ------ execution point ------ #


if __name__ == '__main__':
    main()
    print(get_timestamp(START_TIMER))

# TODO: implement stop playing record (if requires)

