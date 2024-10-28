from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

"""
Импортируем необходимые модули из aiogram:
      Bot — для создания бота.
      Dispatcher — для обработки сообщений.
      types — для работы с типами сообщений и других данных.
      MemoryStorage — для хранения состояний в памяти.
      FSMContext — для работы с контекстом машины состояний.
      State и StatesGroup — для работы с состояниями.
      executor — для запуска бота.
"""

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()     #  Возраст
    growth = State()  #  Рост
    weight = State()  #  Вес

# Создаем клавиатуру
kb = ReplyKeyboardMarkup(resize_keyboard=True)   #  Инициализация клавиатуры kb с автоматическим размером
button1 = KeyboardButton("Рассчитать")   #  Объявление кнопки "Рассчитать"
button2 = KeyboardButton("Информация")   #  Объявление кнопки "Информация"
kb.add(button1, button2)            #  Кнопки добавляются в ряд

@dp.message_handler(commands=['start'])        #  Запуск функции start при вводе команды /start
async def start(message):
    await message.answer('Расчитать', reply_markup=kb)   #  Ответное сообщение и вызов клавиатуры из двух кнопок

@dp.message_handler(text='Рассчитать')         #  Запуск функции set_age при нажатии кнопки 'Расчитать' на клавиатуре
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)   #  Здесь в словаре age - ключ, введенное число - значение ключа
    await message.answer("Введите свой рост")   #  Ответное сообщение
    await UserState.growth.set()                #  Ожидание работы следующего хэндлера

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)   #  Здесь в словаре growth - ключ, введенное число - значение ключа
    await message.answer("Введите свой вес")       #  Ответное сообщение
    await UserState.weight.set()                   #  Ожидание работы следующего хэндлера

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)   #  Здесь в словаре weight - ключ, введенное число - значение ключа
    data = await state.get_data()     # Это элемент, который позволит получить данные состояния (это словарь)
    age = int(data.get("age"))        #  Возраст, значение с ключем "age"
    growth = int(data.get("growth"))  #  Рост, значение с ключем  "growth"
    weight = int(data.get("weight"))  #  Вес, значение с ключем  "weight"
    calories1 = 10 * weight + 6.25 * growth - 5 * age + 5    #  Формула для мужчин
    calories2 = 10 * weight + 6.25 * growth - 5 * age - 161  #  Формула для женщин
    await message.answer(f"Ваша норма калорий (для мужчин): {calories1} ккал.")  #  Считаем норму калорий по формуле
                                                                                 #  Миффлина - Сан Жеора для мужчин
    await message.answer(f"Ваша норма калорий (для женщин): {calories2} ккал.")  #  Считаем норму калорий по формуле
                                                                                 # Миффлина - Сан Жеора для женщин
    await state.finish()  #  Когда машина отработала, ее нужно остановить, чтобы сохранить свое состояние


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  #  Запуск из этого файла