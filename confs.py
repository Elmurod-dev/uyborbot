from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class BotConfig:
    BOT_TOKEN = getenv('BOT_TOKEN')


class WebConfig:
    pass


class PaymentConfig:
    SECRET_KEY = getenv('SECRET_KEY')


class Config:
    bot = BotConfig()
    web = WebConfig()
    payment = PaymentConfig()

