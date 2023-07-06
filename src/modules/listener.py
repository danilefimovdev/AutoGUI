import datetime
import json
import os
import sys
from time import time
import keyboard
from multiprocessing import Process
from typing import NoReturn

from pynput import keyboard as keyboard_, mouse

from config import STOP_RECORDING_HOTKEYS, ROOT_DIR, SWITCH_WINDOW_HOTKEYS
from utils import get_active_window_title, get_timestamp, make_acting_record, get_vk, check_is_window_changed, \
    do_preparation_actions, stop_process

# ------ start time counter ------ #


START_TIMER = time()


# ------ keyboard listening functions ------ #


def on_press(key):
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


def on_release(key):
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


# ------ mouse listening functions ------ #


# TODO: think about should we record every move (offset 1px) or should we write f.e. 1 of five mouse move
# TODO: writing every move would generate huge weight json files
def on_move(x, y):
    """catch mouse movement and write in the log file"""

    # check has the window changed from last action and make record if True
    active_window_title = get_active_window_title()
    check_is_window_changed(active_window_title, START_TIMER)

    # make record of action
    make_acting_record(
        controller="mouse",
        timestamp=get_timestamp(START_TIMER),
        action="move",
        config=dict(x=x, y=y)
    )


def on_click(x, y, button: mouse.Button, pressed):
    """catch mouse clicking and write in the log file"""

    # check has the window changed from last action and make record if True
    active_window_title = get_active_window_title()
    check_is_window_changed(active_window_title, START_TIMER)

    action = "press" if pressed else "release"

    # make record of action

    make_acting_record(
        controller="mouse",
        timestamp=get_timestamp(START_TIMER),
        action=action,
        config=dict(x=x, y=y, button=str(button))
    )


def on_scroll(x: int, y: int, dx: int, dy: int):
    """catch mouse scrolling and write in the log file"""

    # check has the window changed from last action and make record if True
    active_window_title = get_active_window_title()
    check_is_window_changed(active_window_title, START_TIMER)

    # make record of action
    make_acting_record(
        controller="mouse",
        timestamp=get_timestamp(START_TIMER),
        action="scroll",
        config=dict(x=x, y=y, dx=dx, dy=dy)
    )


# ------ hotkey functions ------ #


def write_window_switch() -> NoReturn:

    with open(f'{ROOT_DIR}/involved_in_recording/switch_window_hotkey.json', 'w') as file:
        json.dump(dict(is_pressed=True), file)


# ------ start listening functions ------ #


def start_keyboard_listener():
    """keyboard actions listener"""

    for hotkey in STOP_RECORDING_HOTKEYS:  # set terminate recording hotkeys
        keyboard.add_hotkey(hotkey, stop_process)

    for hotkey in SWITCH_WINDOW_HOTKEYS:   # set window switched flag hotkeys
        keyboard.add_hotkey(hotkey, write_window_switch)

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

