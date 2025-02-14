from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _




def lang_buttons():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text = "English 🇬🇧"),
        KeyboardButton(text = "O'zbek 🇺🇿"),
        KeyboardButton(text = "Русский 🇷🇺"),
        KeyboardButton(text = _("⬅️ back"))
    ])
    rkb.adjust(3 , 1)
    return rkb.as_markup(resize_keyboard= True)

def contact_button():
    contact_btn = KeyboardButton(text = _("☎️ Phone Number") , request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[contact_btn]] , resize_keyboard=True)

def menu_btn():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text = _("📝 Place an ad")),
        KeyboardButton(text = _("🏚 houses for sale")),
        KeyboardButton(text = _("🏘 houses for rent")),
        KeyboardButton(text = _("🏘 my announcements"))
    ])
    rkb.adjust(3 , 1)
    return rkb.as_markup(resize_keyboard= True)

def send_location():
    location_btn = KeyboardButton(text=_("📍 Location"), request_location=True)
    return ReplyKeyboardMarkup(keyboard=[[location_btn]], resize_keyboard=True)

def category_btn():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text = _("🏚 for sale")), # sotish uchun
        KeyboardButton(text = _("🏘 for rent")),
        KeyboardButton(text = _("⬅️ back"))
    ])
    rkb.adjust(2 , 1)
    return rkb.as_markup(resize_keyboard= True)

def place_save_btn():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text = _("✅ Done")),
        KeyboardButton(text = _("⬅️ back"))
    ])
    return rkb.as_markup(resize_keyboard= True)



