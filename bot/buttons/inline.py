from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def make_inline_button():
    regions = [
        "Toshkent", "Qarshi", "Samarqand", "Jizzakh", "Sirdaryo", "Termiz",
        "Xiva", "Nukus", "Farg'ona", "Namangan", "Andijon", "Navoi"
    ]
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text=i, callback_data=i) for i in regions
    ])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()




def house_set_btn(house_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=_("⬅️ Preview"), callback_data='preview'),
        InlineKeyboardButton(text=_("➡️ Next"), callback_data='next'),
        InlineKeyboardButton(text=_("🖼 All Photos"), callback_data=f'all_photos:{house_id}'),
        InlineKeyboardButton(text=_("💲 Sale"), callback_data='sale')
    )
    return keyboard.as_markup()

# def my_house_btn(data : list):
#     ikb = InlineKeyboardBuilder()
#     ikb.add(*[
#         InlineKeyboardButton(text =f"{i}" , callback_data=f"{data[i].id}") for i in range(len(data))
#     ])
#     ikb.adjust(2, repeat=True)
#     return ikb.as_markup()


