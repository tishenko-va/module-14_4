from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from crud_functions import *
import sqlite3


api = "7660573003:AAHSSlMefukzZMRpM-kUneT_w_2wKcTcArA"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)

button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button5 = KeyboardButton(text='Купить')

kb.add(button)
kb.add(button2)
kb.add(button5)

kb2 = InlineKeyboardMarkup()

button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data= 'calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data= 'formulas')

kb2.add(button3)
kb2.add(button4)

kb3 = InlineKeyboardMarkup()

but1 = InlineKeyboardButton(text='Product1', callback_data= 'product_buying')
but2 = InlineKeyboardButton(text='Product2', callback_data= 'product_buying')
but3 = InlineKeyboardButton(text='Product3', callback_data= 'product_buying')
but4 = InlineKeyboardButton(text='Product4', callback_data= 'product_buying')
kb3.add(but1)
kb3.add(but2)
kb3.add(but3)
kb3.add(but4)

all_products = get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()





@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.', reply_markup= kb)

@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup= kb2)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open("1.jpg", "rb") as img:
        await message.answer(f"Название: {all_products[0][0]} | Описание: {all_products[0][1]} | Цена: {all_products[0][2]} руб.")
        await message.answer_photo(img)
    with open("2.jpg", "rb") as img:
        await message.answer(f"Название: {all_products[1][0]} | Описание: {all_products[1][1]} | Цена: {all_products[1][2]} руб.")
        await message.answer_photo(img)
    with open("3.jpg", "rb") as img:
        await message.answer(f"Название: {all_products[2][0]} | Описание: {all_products[2][1]} | Цена: {all_products[2][2]} руб.")
        await message.answer_photo(img)
    with open("4.jpg", "rb") as img:
        await message.answer(f"Название: {all_products[3][0]} | Описание: {all_products[3][1]} | Цена: {all_products[3][2]} руб.")
        await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb3)



@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()



@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()



@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)