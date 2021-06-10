from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):

    region = State()
    models = State()
    price_to = State()
    price_from = State()
    view = State()



