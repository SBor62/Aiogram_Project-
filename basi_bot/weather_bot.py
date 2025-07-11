import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
import requests
import random

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Добавляем определение logger

# Загружаем переменные окружения
load_dotenv()

# Получаем токены
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWM_API_KEY = os.getenv('OWM_API_KEY')

# Проверка наличия токенов
if not BOT_TOKEN or not OWM_API_KEY:
    logger.error("Не указаны BOT_TOKEN или OWM_API_KEY в переменных окружения!")
    exit(1)

# Инициализация бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "<b>Привет!</b> Я бот погоды.\n"
        "Отправь /weather для прогноза в <i>Москве</i>"
    )


@dp.message(Command("photo"))
async def photo(message: types.Message):
    list = [
        'https://cs9.pikabu.ru/post_img/big/2018/03/22/6/1521710988188123266.jpg',
        'https://i.pinimg.com/736x/8d/a4/8f/8da48feabf62ca030ff36a281c5b41a0.jpg',
        'https://i.pinimg.com/736x/d2/1a/3c/d21a3c2e9c55b341c091e0bbe1ac9308.jpg',
        'https://i.pinimg.com/originals/f6/90/60/f69060a84a11f871c12d91818c952d80.jpg',
        'https://cs.pikabu.ru/post_img/big/2013/07/03/4/1372820730_1017112159.png'
    ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это забавная картинка')


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "Команды:\n/start - Начать\n/help - Помощь\n/weather - Погода в Москве\n/photo - Случайное фото котят"
    )


@dp.message(Command("weather"))
async def get_weather(message: types.Message):
    lat, lon = 55.7558, 37.6173  # Координаты Москвы
    url = (f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}"
           f"&appid={OWM_API_KEY}&units=metric&lang=ru")

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_info = (
                f"🌆 Погода в Москве:\n"
                f"☁️ {data['weather'][0]['description'].capitalize()}\n"
                f"🌡️ {data['main']['temp']}°C (ощущается как {data['main']['feels_like']}°C)\n"
                f"💧 Влажность: {data['main']['humidity']}%"
            )
        else:
            weather_info = "❌ Ошибка при получении данных."
    except Exception as e:
        logger.error(f"Ошибка при запросе погоды: {e}")  # Используем logger вместо print
        weather_info = "⚠️ Ошибка при получении данных о погоде."

    await message.answer(weather_info)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
