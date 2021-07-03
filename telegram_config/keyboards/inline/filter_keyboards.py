from aiogram import types
from salecars.models import Region, City
from salecars.models import Marks, Models, Users


def start_filter_keyboard():
    btn_text = (('Добавить', 'add'), ('Удалить', 'delete'))
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


def delete_filters_keyboard(telegram_id):
    filters = Users.get_filters(telegram_id)
    btn_text = ((f'{_filter.marks.name} {_filter.model.name}', _filter.id) for _filter in filters)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    btn = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_text)
    return keyboard_markup.add(*btn)



