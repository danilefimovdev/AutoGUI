from typing import NoReturn

from defaullts import LANGUAGES
from utils import get_keyboard_language, activate_window


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



