from aiogram import types
from salecars.models import Region, City
from salecars.models import Marks, Models


def start_keyboard():
    btn_text = (('Поиск', 'search'), ('Подать', 'send'), ('Личный фильтр', 'filter'))
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def register_keyboard():
    btn_text = (('Регистрация', 'register'), ('Еще не придумал)', '0'), ('Тоже', '1'))
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def region_keyboard():
    regions = Region.objects.all()
    btn_text = ((region.name, region.id) for region in regions)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def city_keyboard(region_id):
    citys = City.objects.filter(region=region_id)
    btn_text = ((city.name, city.id) for city in citys)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def marks_keyboard():
    marks = Marks.objects.all()
    btn_text = ((mark.name, mark.id) for mark in marks)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def models_keyboard(mark_id):
    models = Models.objects.filter(mark=mark_id)
    btn_text = ((model.name, model.id) for model in models)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def paginations_keyboard(count_pages, count=1):
    btn_text = (('⬅', 'prev'), (f"{count} из {count_pages}", " "), ('➡', 'next'))
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def true_and_false_keyboard():
    btn_text = (('Да', 'True'), ('Нет', 'False'))
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def wheel_choices_keyboard():
    btn_text = (('Слева', 'LEFT'), ('Справа', 'RIGHT'))
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def engine_keyboard():
    btn_text = (
        ('Газ', 'GAS'),
        ('Бензин', 'BENZ'),
        ('Газ-бензин', 'GAS_BENZ'),
        ('Дизель', 'DIESEL'),
        ('Электро', 'ELECTRO')
    )
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)


def phone_keyboard():
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton('Поделиться номером', request_contact=True)
    return keyboard_markup.add(btn)




