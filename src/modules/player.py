import json
import logging
import sys
from time import sleep

import keyboard
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, KeyCode
from win32api import GetKeyState

from utils import activate_window, get_timestamp, stop_process, ask_user_for_a_record_name, get_keyboard_language, \
    get_current_datetime, get_open_windows
from defaullts import ROOT_DIR, MOUSE_BUTTONS, LANGUAGES


# ------ mouse actions ------


MOUSE = MouseController()


def move_to(config: dict) -> None:
    """ change mouse position """

    try:
        MOUSE.position = (config['x'], config['y'])
    except Exception as ex:
        raise ex


def press_mouse(config: dict) -> None:
    """ press mouse button """

    try:
        if MOUSE.position != (config['x'], config['y']):
            move_to(config)
        MOUSE.press(MOUSE_BUTTONS[config['button']])
    except Exception as ex:
        raise ex


def release_mouse(config: dict) -> None:
    """ release mouse button """

    try:
        if MOUSE.position != (config['x'], config['y']):
            move_to(config)
        MOUSE.release(MOUSE_BUTTONS[config['button']])
    except Exception as ex:
        raise ex


def scroll_mouse(config: dict) -> None:
    """ do mouse scroll """

    try:
        if MOUSE.position != (config['x'], config['y']):
            move_to(config)
        dx = 0
        MOUSE.scroll(dx, config['dy'])
    except Exception as ex:
        raise ex


MOUSE_ACTIONS = {
    'scroll': scroll_mouse,
    'press': press_mouse,
    'release': release_mouse,
    'move': move_to
}


# ------ keyboard actions ------ #


KEYBOARD = KeyboardController()


def press_keyboard(config: dict) -> None:
    """ press keyboard key """

    try:
        key_code = KeyCode.from_vk(config['key'])
        KEYBOARD.press(key_code)
    except Exception as ex:
        raise ex


def release_keyboard(config: dict) -> None:
    """ release keyboard key """

    try:
        key_code = KeyCode.from_vk(config['key'])
        KEYBOARD.release(key_code)
    except Exception as ex:
        raise ex


def toggle_capslock(config: dict) -> None:

    caps_lock_vk = 20

    try:
        is_caps_lock_toggled = GetKeyState(caps_lock_vk)
        if is_caps_lock_toggled != config['is_toggled']:
            key_code = KeyCode.from_vk(caps_lock_vk)
            KEYBOARD.press(key_code)
            KEYBOARD.release(key_code)
    except Exception as ex:
        raise ex


KEYBOARD_ACTIONS = {
    'press': press_keyboard,
    'release': release_keyboard,
    'toggle_capslock': toggle_capslock,
}


# ------ special actions ------ #


def switch_window(config: dict) -> None:
    """ switch to the window with passed title if the window exists """

    try:
        activate_window(config['title'])
    except Exception as ex:
        raise ex


def check_are_required_windows_opened(config: dict) -> None:
    """check if all required for playing log windows are opened"""

    current_opened_windows_title = get_open_windows()
    required_windows_to_be_opened = set(config['windows'])
    if not required_windows_to_be_opened.issubset(current_opened_windows_title):
        windows_to_open = required_windows_to_be_opened.difference(current_opened_windows_title)
        window_titles = []
        for title in windows_to_open:
            window_titles.append(str(title))
            # window_titles.append(unicode(someString, 'utf-8', errors='ignore'))
        print('window_titles', window_titles)
        raise Exception(f'Next windows must be opened to start play log: {window_titles}')


def check_language(config: dict) -> None:

    try:
        current_lang = get_keyboard_language()
        lang_name = LANGUAGES[config['lang_id']]
        if current_lang != config['lang_id']:
            raise Exception(f'Wrong keyboard layout. Change it to "{lang_name}"')
    except Exception as ex:
        raise ex


SPECIAL_ACTIONS = {
    'check_language': check_language,
    'activate_window': activate_window,
    'check_are_required_windows_opened': check_are_required_windows_opened,
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

            limit = (len(file.readlines()) - acts_to_ignore)
            file.seek(0)  # move reading cursor to the beginning of the file
            for line in file.readlines()[0:limit]:
                item = json.loads(line)

                # here we are waiting when action time would be equal or less than start script time
                while item['timestamp'] > get_timestamp():
                    sleep(pause)
                # when the time is right we start the action
                if item['controller'] == 'mouse':
                    MOUSE_ACTIONS[item['action']](item['config'])
                elif item['controller'] == 'keyboard':
                    KEYBOARD_ACTIONS[item['action']](item['config'])
                else:  # special (language change, window switch)
                    SPECIAL_ACTIONS[item['action']](item['config'])
        print(f'Finished playing {file_name}')
    except Exception as ex:

        logging.basicConfig(level=logging.INFO, filename=f'{ROOT_DIR}/logs/{get_current_datetime()}_play_error.log', filemode="w")
        logging.info(msg=item)
        logging.error(str(ex), exc_info=True)

        # print(f" Error has occurred. Check {get_current_datetime()}_play_error.log for detail info ! ")
        print(ex)
    finally:
        sys.exit()


# ------ execution point ------ #


if __name__ == '__main__':
    main()
