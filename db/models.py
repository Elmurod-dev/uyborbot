from pydantic.v1 import validator

from bot.enums import LangEnum
from db.config import DB


class User(DB):
    def __init__(self,*cols,
                 id = None,
                 full_name = None,
                 phone_number = None,
                 lang = LangEnum.en.name):
        self.cols = cols
        self.id = id
        self.full_name = full_name
        self.phone_number = phone_number
        self.lang = lang


    @classmethod
    @validator('phone_number')
    async def phone_number_validator(cls, phone_number):
        if phone_number.startswith("+"):
            return phone_number[1:]
        return phone_number







class House(DB):
    def __init__(self,*cols,
                 id = None,
                 address = None,
                 area = None,
                 price = None,
                 room = None,
                 latitute = None,
                 longitute = None,
                 user_id = None,
                 status = None,
                 pictures = None,
                 category = None):
        self.cols = cols
        self.id = id
        self.address = address
        self.area = area
        self.price = price
        self.room = room
        self.latitute = latitute
        self.longitute = longitute
        self.user_id = user_id
        self.status = status
        self.pictures = pictures
        self.category = category


"""
Toshkent
Qarshi
Samarqand
Jizzakh
Sirdaryo
Termiz
Xiva
Nukus
Farg'ona
Namangan
Andijon
Navoi
"""

# print(Addres().select(id=2))
# print(House().select(category='🏘 for rent'))
# a = Addres().select(id=2)
# print(a[0].name)
# a = House().houses_pagination(6203274805,1)
# print(a)

# print(House().houses_pagination(page_num=1,user_id=6203274805)[0].category)
