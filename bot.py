import random
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from config import TOKEN
from compliments import beauty, character, romantic, random_thoughts


bot = Bot(token=TOKEN)
dp = Dispatcher()


# хранение уже отправленных комплиментов
used_compliments = {}


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌸 Про внешность"), KeyboardButton(text="✨ Про характер")],
        [KeyboardButton(text="💌 Что я думаю о тебе"), KeyboardButton(text="🎲 Случайный комплимент")]
    ],
    resize_keyboard=True
)


def get_unique_compliment(user_id, compliments):

    if user_id not in used_compliments:
        used_compliments[user_id] = []

    available = list(set(compliments) - set(used_compliments[user_id]))

    if not available:
        used_compliments[user_id] = []
        available = compliments

    compliment = random.choice(available)

    used_compliments[user_id].append(compliment)

    return compliment


@dp.message(Command("start"))
async def start(message: Message):

    text = (
        "Привет, Вишенка.\n"
        "Я сделал небольшой бот.\n"
        "Он иногда говорит тебе приятные вещи.\n"
        "Можешь нажать любую кнопку и проверить."
    )

    await message.answer(text, reply_markup=keyboard)


@dp.message(F.text == "🌸 Про внешность")
async def beauty_handler(message: Message):

    compliment = get_unique_compliment(message.from_user.id, beauty)
    await message.answer(compliment)


@dp.message(F.text == "✨ Про характер")
async def character_handler(message: Message):

    compliment = get_unique_compliment(message.from_user.id, character)
    await message.answer(compliment)


@dp.message(F.text == "💌 Что я думаю о тебе")
async def romantic_handler(message: Message):

    compliment = get_unique_compliment(message.from_user.id, romantic)
    await message.answer(compliment)


@dp.message(F.text == "🎲 Случайный комплимент")
async def random_handler(message: Message):

    all_compliments = beauty + character + romantic + random_thoughts

    # иногда отправляем длинную мысль
    if random.randint(1, 8) == 1:
        compliment = get_unique_compliment(message.from_user.id, random_thoughts)
    else:
        compliment = get_unique_compliment(message.from_user.id, all_compliments)

    await message.answer(compliment)


async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())