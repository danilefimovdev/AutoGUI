import datetime
import os
import sys
from time import time
from multiprocessing import Process

from pynput import keyboard as keyboard_, mouse

from mouse_actions import on_click, on_move, on_scroll
from src.modules.keyboard_actions import on_press, on_release
from utils import do_preparation_actions, set_hotkeys
from defaullts import ROOT_DIR


# ------ start time counter ------ #


START_TIMER = time()


# ------ start listening functions ------ #


def start_keyboard_listener():
    """keyboard actions listener"""

    set_hotkeys()

    with keyboard_.Listener(
            on_press=on_press,
            on_release=on_release
    ) as listener:
        listener.join()


def start_mouse_listener():
    """mouse actions listener"""

    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll
    ) as listener:
        listener.join()


# ------ execution function ------ #


def main():
    """main function"""

    # str representation of start listening for record name
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print('Start recording')
    try:

        do_preparation_actions(START_TIMER)

        # create processes for listening both mouse and keyboard
        mouse_list_proc = Process(target=start_mouse_listener)
        keyboard_list_proc = Process(target=start_keyboard_listener)

        # start each process
        mouse_list_proc.start()
        keyboard_list_proc.start()

        # wait when hotkey listener process would be terminated (certain hotkey comb terminate it)
        keyboard_list_proc.join()

        # when one listener has been terminated we do not need to listen others anymore
        mouse_list_proc.terminate()

    except Exception as ex:
        print(ex)

    finally:
        # set start listening time as a file name
        record_name = f'{current_datetime}.json'
        os.rename(f'{ROOT_DIR}/records/input_file.json', f"{ROOT_DIR}/records/{record_name}")
        print('Recorded!')
        print(f"Your record file: {record_name}")
        sys.exit()


# ------ execution point ------ #


if __name__ == '__main__':
    main()

