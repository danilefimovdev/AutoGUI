from typing import NoReturn

from pynput.mouse import Controller, Button

from src.modules.defaullts import MOUSE_BUTTONS
from src.modules.utils import get_active_window_title, check_is_window_changed, make_acting_record, get_timestamp


# ------ mouse listening functions ------ #


# TODO: think about should we record every move (offset 1px) or should we write f.e. 1 of five mouse move
# TODO: writing every move would generate huge weight json files
def on_move(x, y, START_TIMER: float):
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


def on_click(x, y, button: Button, pressed, START_TIMER: float) -> NoReturn:
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


def on_scroll(x: int, y: int, dx: int, dy: int, START_TIMER: float) -> NoReturn:
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


# ------ mouse playing functions ------ #


def move_to(config: dict, controller: Controller) -> NoReturn:
    """ change mouse position """

    controller.position = (config['x'], config['y'])


def press_mouse(config: dict, controller: Controller) -> NoReturn:
    """ press mouse button """

    if controller.position != (config['x'], config['y']):
        move_to(config, controller)
    controller.press(config['button'])


def release_mouse(config: dict, controller: Controller) -> NoReturn:
    """ release mouse button """

    if controller.position != (config['x'], config['y']):
        move_to(config, controller)
    controller.release(MOUSE_BUTTONS[config['button']])


def scroll_mouse(config: dict, controller: Controller) -> NoReturn:
    """ do mouse scroll """

    if controller.position != (config['x'], config['y']):
        move_to(config, controller)
    dx = 0
    controller.scroll(dx, config['dy'])
