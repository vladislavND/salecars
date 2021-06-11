from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):

    region = State()
    city = State()
    marks = State()
    models = State()
    price = State()
    view = State()



