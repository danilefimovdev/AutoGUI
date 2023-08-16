import os
import sys
from multiprocessing import Process
from typing import NoReturn
from pynput import keyboard as keyboard_, mouse
from pynput.mouse import Button

from utils import do_preparation_actions, set_hotkeys, get_active_window_title, make_acting_record, get_vk, \
    check_is_window_changed, get_current_datetime
from defaullts import ROOT_DIR
import logging


move_counter = 1


# ------ keyboard listening functions ------ #


def on_press(key) -> NoReturn:
    """catch keyboard's key pressing and write in the log file"""

    # print("on_press")

    try:
        vk = get_vk(key)
        # check has the window changed from the last action and make record if True

        if vk != 9:
            active_window_title = get_active_window_title()
            check_is_window_changed(active_window_title)

        # make record of action
        make_acting_record(
            controller="keyboard",
            action="press",
            config=dict(key=vk)
        )
    except Exception as ex:
        raise Exception(ex)


def on_release(key) -> NoReturn:
    """catch keyboard's key releasing and write in the log file"""

    # print("on_release")

    # check has the window changed from last action and make record if True
    active_window_title = get_active_window_title()
    check_is_window_changed(active_window_title)

    # make record of action
    make_acting_record(
        controller="keyboard",
        action="release",
        config=dict(key=get_vk(key))
    )


# ------ mouse listening functions ------ #


def on_move(x, y):
    """catch mouse movement and write in the log file"""
    global move_counter
    # print("on_move")

    try:
        active_window_title = get_active_window_title()
        check_is_window_changed(active_window_title)

        # make record of action
        if move_counter % 10 == 0:
            make_acting_record(
                controller="mouse",
                action="move",
                config=dict(x=x, y=y)
            )
        move_counter += 1
    except Exception as ex:
        raise Exception(ex)


def on_click(x, y, button: Button, pressed) -> NoReturn:
    """catch mouse clicking and write in the log file"""

    action = "press" if pressed else "release"
    # print(f"on_click_{action}")

    try:
        active_window_title = get_active_window_title()
        check_is_window_changed(active_window_title)

        # make record of action

        make_acting_record(
            controller="mouse",
            action=action,
            config=dict(x=x, y=y, button=str(button))
        )
    except Exception as ex:
        raise Exception(ex)


def on_scroll(x: int, y: int, dx: int, dy: int) -> NoReturn:
    """catch mouse scrolling and write in the log file"""

    # print("on_scroll")

    try:
        active_window_title = get_active_window_title()
        check_is_window_changed(active_window_title)
        # make record of action
        make_acting_record(
            controller="mouse",
            action="scroll",
            config=dict(x=x, y=y, dx=dx, dy=dy)
        )
    except Exception as ex:
        raise Exception(ex)

# ------ start listening functions ------ #


def start_keyboard_listener():
    """keyboard actions listener"""

    set_hotkeys(window_switch=True, stop_recording=True)
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
            on_scroll=on_scroll,
    ) as listener:
        listener.join()


# ------ execution function ------ #


def main():
    """main function"""

    # str representation of start listening for record name
    current_datetime = get_current_datetime()
    print('Start recording')

    try:
        do_preparation_actions()

        # create processes for listening both mouse and keyboard
        mouse_list_proc = Process(target=start_mouse_listener)
        keyboard_list_proc = Process(target=start_keyboard_listener)

        # start each process.
        mouse_list_proc.start()
        keyboard_list_proc.start()

        # wait when hotkey listener process would be terminated (certain hotkey comb terminate it)
        keyboard_list_proc.join()

        # when one listener has been terminated we do not need to listen others anymore
        mouse_list_proc.terminate()

    except Exception as ex:
        logging.basicConfig(level=logging.INFO, filename=f'{ROOT_DIR}/logs/{get_current_datetime()}_record_error.log', filemode="w")
        logging.error(ex, exc_info=True)
        print(f" Error has occurred. Check {get_current_datetime()}_record_error.log for detail info ! ")
    finally:
        # set start listening time as a file name
        record_name = f'{current_datetime}.json'
        os.rename(f'{ROOT_DIR}/records/input_file.json', f"{ROOT_DIR}/records/{record_name}")
        print("Recorded!", f"Your record file: {record_name}", sep="\n")
        sys.exit()


# ------ execution point ------ #


if __name__ == '__main__':
    main()
