from aiogram import types
from salecars.models import Region, City
from salecars.models import Marks, Models


def search_keyboard():

    btn_text = (('ford', '0'), ('Москвич', '1'))
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)
