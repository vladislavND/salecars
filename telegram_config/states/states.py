from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):

    region = State()
    city = State()
    marks = State()
    models = State()
    price = State()
    crash = State()
    engine = State()
    value = State()
    year = State()
    steering_wheel = State()
    description = State()
    resident = State()
    image = State()
    phone = State()
    view = State()


class SettingsState(StatesGroup):

    mobile_phone = State()


class FilterState(StatesGroup):
    region = State()
    city = State()
    marks = State()
    models = State()
    price_to = State()
    price_from = State()
    crash = State()
    engine = State()
    value = State()
    year = State()
    steering_wheel = State()
    resident = State()
    add = State()
    delete = State()
    choice = State()






