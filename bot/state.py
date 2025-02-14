from aiogram.fsm.state import StatesGroup, State


class ButtonsState(StatesGroup):
    lang = State()

class PlaceState(StatesGroup):
    address = State()
    area = State()
    price = State()
    room = State()
    pictures = State()
    location = State()
    category = State()
    waiting_for_picture = State()

class PaginationState(StatesGroup):
    page_num = State()
    category = State()




