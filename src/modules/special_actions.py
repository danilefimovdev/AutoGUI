import json
from typing import NoReturn

from src.modules.defaullts import LANGUAGES, ROOT_DIR
from src.modules.utils import get_keyboard_language, activate_window


# ------ special playing functions ------ #


def check_language(config: dict) -> NoReturn:

    current_lang = get_keyboard_language()
    lang_name = LANGUAGES[config['lang_id']]
    if current_lang != config['lang_id']:
        raise Exception(f'Wrong keyboard layout. Change it to "{lang_name}"')


def switch_window(config: dict) -> NoReturn:
    """ switch to the window with passed title if the window exists """

    try:
        activate_window(config['title'])
    except Exception as ex:
        raise ex


# ------ special playing functions ------ #


def write_window_switch() -> NoReturn:

    with open(f'{ROOT_DIR}/involved_in_recording/switch_window_hotkey.json', 'w') as file:
        json.dump(dict(is_pressed=True), file)


