import logging

from aiogram import Router, F, Bot
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.inline import make_inline_button, house_set_btn
from bot.buttons.reply import contact_button, menu_btn, category_btn, place_save_btn
from bot.enums import LangEnum
from bot.state import PlaceState
from confs import Config
from db.models import User, House

logging.basicConfig(
    filename='bot/bot_main.log',   # Xatolar yoziladigan fayl nomi
    level=logging.ERROR,     # Xatolarni qayd qilish darajasi
    format='%(asctime)s - %(levelname)s - %(message)s'  # Yozish formati
)



TOKEN = Config.bot.BOT_TOKEN
bot = Bot(TOKEN)
main_router = Router()
@main_router.message(F.text == __('⬅️ back'))
@main_router.message(CommandStart())
async def Command_start_handler(message: Message,state: FSMContext):
    await state.clear()
    user: list[User] = User().select(id=message.from_user.id)
    if not user:
        await message.answer(text=_('Hello, welcome to Uybor bot!'),reply_markup =  contact_button())
    else:
        await message.answer(text=_("Menu"),reply_markup=menu_btn())


@main_router.message(lambda message: message.contact is not None)
async def handle_contact(message: Message):
    contact = message.contact
    User(id=message.from_user.id, full_name=message.from_user.full_name, lang=LangEnum.en.name,
         phone_number=contact.phone_number).insert()
    await message.answer(text=_("You have successfully registered!"), reply_markup=menu_btn())


@main_router.message(F.text == __("📝 Place an ad"))
async def handle_state(message: Message, state: FSMContext):
    await message.answer(text=_("Select category: "), reply_markup=category_btn())
    await state.set_state(PlaceState.category)


@main_router.message(PlaceState.category)
async def handle_category(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)
    await message.answer(text=_("Select region or city: "), reply_markup=make_inline_button())
    await state.set_state(PlaceState.address)


@main_router.callback_query(PlaceState.address)
async def handle_address(callback: CallbackQuery, state: FSMContext):
    await state.update_data(address=callback.data)
    await callback.message.answer(text=_("Area of the house (m*m): "))
    await state.set_state(PlaceState.area)


@main_router.message(PlaceState.area)
async def handle_area(message: Message, state: FSMContext):
    await state.update_data(area=message.text)
    await state.set_state(PlaceState.price)
    await message.answer(text=_("The price of the house ($) minimal (100$): "))


@main_router.message(PlaceState.price)
async def handle_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(PlaceState.room)
    await message.answer(text=_("How many rooms does the house have?: "))


@main_router.message(PlaceState.room)
async def handle_room(message: Message, state: FSMContext):
    await state.update_data(room=message.text)
    await state.set_state(PlaceState.location)
    await message.answer(text=_("Send your home location: "))


@main_router.message(PlaceState.location)
async def handle_location(message: Message, state: FSMContext):
    await state.update_data(location=message.location)
    await state.set_state(PlaceState.pictures)
    await message.answer(text=_("Send a picture of your house or press 'done' if you're finished: "))


@main_router.message(PlaceState.pictures)
async def handle_pictures(message: Message, state: FSMContext):
    await state.set_state(PlaceState.waiting_for_picture)
    await message.answer(text=_("Send a picture of your house or press 'done' if you're finished."),reply_markup=place_save_btn())


@main_router.message(PlaceState.waiting_for_picture)
async def handle_waiting_for_picture(message: Message, state: FSMContext):
    # "done" tugmasini tekshirish uchun faqat matnli xabarlar bo'yicha ish tutamiz
    if message.text and message.text == '✅ Done':
        # Foydalanuvchi "done" tugmasini bosdi
        house_data = await state.get_data()
        pictures = house_data.get('pictures', '').strip(',')  # Oxirgi vergulni olib tashlaymiz

        # Ma'lumotlarni saqlash
        House(
            area=house_data['area'],
            price=house_data['price'],
            room=house_data['room'],
            pictures=pictures,  # Birlashtirilgan rasmlar
            longitute=house_data['location'].longitude,
            latitute=house_data['location'].latitude,
            user_id=message.from_user.id,
            address=house_data['address'],
            category=house_data['category']
        ).insert()

        await message.answer(_("Thank you! Your ad has been submitted."), reply_markup=menu_btn())
        await state.clear()  # Holatni tozalash
    else:
        # Rasm yuborilsa
        if message.photo:
            try:
                file_id = message.photo[-1].file_id  # Oxirgi rasm file_id sini olish
                current_pictures = (await state.get_data()).get('pictures', '')
                await state.update_data(pictures=current_pictures + ',' + file_id)  # Rasm file_id larini yangilash
                await message.answer(text=_("Picture added! Send another picture or press 'done' to finish."),reply_markup=place_save_btn())
            except Exception:
                await message.answer(text=_("An error occurred while adding the picture!"))
        else:
            await message.answer(
                text=_("You did not send a file, please send a picture of your house or 'done' to finish!"))





# 🏘 my announcements handler
@main_router.message(F.text == __('🏘 my announcements'))
async def handle_state(message: Message, state: FSMContext):
    user_houses = House().houses_pagination(page_num=1, user_id=message.from_user.id)
    if user_houses:
        house = user_houses[0]
        await message.answer_photo(
            photo=house.pictures.split(',')[0],
            caption=(f"Category: {house.category}\n"
                     f"Room: {house.room}\n"
                     f"Address 📍: {house.address}\n"
                     f"Price 💵: {house.price}$\n"
                     f"Status: {house.status}\n"
                     f"User Phone_number: {User().select(id=house.user_id)[0].phone_number}"),
            reply_markup=house_set_btn(house_id=house.id)
        )
        await state.update_data(page_num=2, category='my_announcements')  # Bo'lim turi qo'shildi
    else:
        await message.answer(text=_('ads are over'))


# 🏚 houses for sale handler
@main_router.message(F.text == __('🏚 houses for sale'))
async def handle_state(message: Message, state: FSMContext):
    houses = House().houses_pagination(page_num=1, category='🏚 for sale')

    if houses:
        house = houses[0]
        await message.answer_photo(
            photo=house.pictures.split(',')[0],
            caption=(f"Category: {house.category}\n"
                     f"Room: {house.room}\n"
                     f"Address 📍: {house.address}\n"
                     f"Price 💵: {house.price}$\n"
                     f"Status: {house.status}\n"
                     f"User Phone_number: {User().select(id=house.user_id)[0].phone_number}"),
            reply_markup=house_set_btn(house.id)
        )
        await state.update_data(page_num=2, category='for_sale')  # Bo'lim turi qo'shildi
    else:
        await message.answer(text=_('ads are over'))


# 🏘 houses for rent handler
@main_router.message(F.text == __('🏘 houses for rent'))
async def handle_state(message: Message, state: FSMContext):
    houses = House().houses_pagination(page_num=1, category='🏘 for rent')

    if houses:
        house = houses[0]
        await message.answer_photo(
            photo=house.pictures.split(',')[0],
            caption=(f"Category: {house.category}\n"
                     f"Room: {house.room}\n"
                     f"Address 📍: {house.address}\n"
                     f"Price 💵: {house.price}$\n"
                     f"Status: {house.status}\n"
                     f"User Phone_number: {User().select(id=house.user_id)[0].phone_number}"),
            reply_markup=house_set_btn(house_id=house.id)
        )
        await state.update_data(page_num=2, category='for_rent')  # Bo'lim turi qo'shildi
    else:
        await message.answer(text=_("ads are over"))


# Callback query handler (Next tugmasi uchun)
@main_router.callback_query(lambda c: c.data == 'next')
async def handle_next(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data.get('page_num', 1)
    category = data.get('category')  # Bo'lim turini olish
    if category == 'my_announcements':
        # Foydalanuvchining e'lonlarini ko'rsatish
        houses = House().houses_pagination(page_num=current_page, user_id=callback_query.from_user.id)
    elif category == 'for_sale':
        # Sotuvga qo'yilgan e'lonlarni ko'rsatish
        houses = House().houses_pagination(page_num=current_page, category='🏚 for sale')
    elif category == 'for_rent':
        # Ijaraga berilayotgan e'lonlarni ko'rsatish
        houses = House().houses_pagination(page_num=current_page, category='🏘 for rent')

    if houses:
        house = houses[0]
        await callback_query.message.delete()
        await bot.send_photo(
            chat_id=callback_query.from_user.id,
            photo=house.pictures.split(',')[0],
            caption=(f"Category: {house.category}\n"
                     f"Room: {house.room}\n"
                     f"Address 📍: {house.address}\n"
                     f"Price 💵: {house.price}$\n"
                     f"Status: {house.status}\n"
                     f"User Phone_number: {User().select(id=house.user_id)[0].phone_number}"),
            reply_markup=house_set_btn(house.id)
        )
        await state.update_data(page_num=current_page + 1)
    else:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=_("ads are over"),
            reply_markup=menu_btn()
        )


# Callback query handler (Preview tugmasi uchun)
@main_router.callback_query(lambda c: c.data == 'preview')
async def handle_preview(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data.get('page_num', 2)  # Dastlabki sahifani oling, default 2 qilamiz, chunki 1-sahifa mavjud

    if current_page > 1:  # 1-sahifadan orqaga qaytish mumkin emas
        previous_page = current_page - 1
        category = data.get('category')  # Bo'lim turini olish

        # Oldingi e'lonlarni olish
        if category == 'my_announcements':
            houses = House().houses_pagination(page_num=previous_page, user_id=callback_query.from_user.id)
        elif category == 'for_sale':
            houses = House().houses_pagination(page_num=previous_page, category='🏚 for sale')
        elif category == 'for_rent':
            houses = House().houses_pagination(page_num=previous_page, category='🏘 for rent')

        if houses:
            house = houses[0]

            # Oldingi xabarni o'chirish
            await callback_query.message.delete()

            # Oldingi e'lonni ko'rsatish
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=house.pictures.split(',')[0],
                caption=(f"Category: {house.category}\n"
                         f"Room: {house.room}\n"
                         f"Address 📍: {house.address}\n"
                         f"Price 💵: {house.price}$\n"
                         f"Status: {house.status}"),
                reply_markup=house_set_btn(house.id)  # Inline tugmalar
            )

            # Sahifani yangilash
            await state.update_data(page_num=previous_page)
        else:
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=_("ads are over"),
                reply_markup=menu_btn()
            )
    else:
        await callback_query.answer(_("This is the first announcement"), show_alert=True)




@main_router.callback_query(F.data.startswith('all_photos:'))
async def view_all_photos(callback: CallbackQuery):
    house_id = callback.data.split(':')[1]
    house = House().select(id=house_id)  # Bu yerda house ma'lumotlarini olish

    if house:
        pictures = house[0].pictures.split(',')  # Rasmlarni ajratamiz

        # Rasmlarni InputMediaPhoto formatida tayyorlash
        media = [InputMediaPhoto(media=picture) for picture in pictures]

        # Media group sifatida yuborish
        await callback.message.answer_media_group(media=media)
    else:
        await callback.answer(_("No pictures found for this house."))  # Agar rasm bo'lmasa
    await callback.answer()  # Callback ni tasdiqlash
