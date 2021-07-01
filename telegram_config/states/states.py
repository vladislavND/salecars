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
    register = State()



