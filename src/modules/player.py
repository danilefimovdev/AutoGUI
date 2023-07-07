import json
import sys
from time import time, sleep

import keyboard
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from keyboard_actions import press_keyboard, release_keyboard, toggle_capslock
from mouse_actions import scroll_mouse, press_mouse, release_mouse, move_to
from special_actions import check_language
from utils import activate_window, get_timestamp, stop_process, ask_user_for_a_record_name
from defaullts import ROOT_DIR


# ------ start time counter ------ #


START_TIMER = time()


# ------ mouse setting ------ #


MOUSE = MouseController()

MOUSE_ACTIONS = {
    'scroll': scroll_mouse,
    'press': press_mouse,
    'release': release_mouse,
    'move': move_to
}


# ------ keyboard setting ------ #


KEYBOARD = KeyboardController()

KEYBOARD_ACTIONS = {
    'press': press_keyboard,
    'release': release_keyboard,
    'toggle_capslock': toggle_capslock,
}


# ------ special setting ------ #


SPECIAL_ACTIONS = {
    'check_language': check_language,
    'activate_window': activate_window
}


# ------ main function ------ #


def main():

    # set terminate playing hotkeys
    with open(f'{ROOT_DIR}/used_in_recording_&_playing/config.json', mode='r') as file:
        config = json.load(file)

        # TODO: think how we can pass the length of stop recording hotkey dynamically
        # TODO: or find out how we can remove records of pressing stop record hotkey from the end
        hotkeys = config["STOP_RECORDING_HOTKEYS"]
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

            file.seek(0)  # move reading cursor to the beginning of the file
            for line in file.readlines()[0:acts_to_ignore]:
                item = json.loads(line)

                # here we are waiting when action time would be equal or less than start script time
                while item['timestamp'] > get_timestamp(START_TIMER):
                    sleep(pause)
                error_timestamp = item['timestamp']
                # when the time is right we start the action
                if item['controller'] == 'mouse':
                    MOUSE_ACTIONS[item['action']](item['config'], MOUSE)
                elif item['controller'] == 'keyboard':
                    KEYBOARD_ACTIONS[item['action']](item['config'], KEYBOARD)
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


