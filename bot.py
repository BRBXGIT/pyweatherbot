from config import tg_token, token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import BotDB
from new_city import Ask
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#Всякие константы
BotDB = BotDB('citys.db')
bot = Bot(token=tg_token)
dp = Dispatcher(bot, storage=MemoryStorage())


#Обработчик команды старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	BotDB.add_user(message.from_user.id)
	await message.reply('Привет, если ты напишешь мне название города, я покажу его погоду\n\n'
						'Что-бы создать кнопку с твоим городом введи /new_city , а после название города. Так будет удобнее)')


#Перемещение пользователя в состояние ввода города
@dp.message_handler(commands=['new_city'])
async def add_city(message: types.Message):
	await message.answer('Введите ваш город: ')
	await Ask.Q1.set()


#Добавление пользователя в бд и заполнение кнопки с городом
@dp.message_handler(state=Ask.Q1)
async def add_to_db(message: types.Message, state: FSMContext):
	answer = message.text
	BotDB.add_city(message.from_user.id, answer)

	city = str(BotDB.get_city(message.from_user.id)).strip("'[](),'")

	all_keyboard = ReplyKeyboardMarkup(
	keyboard = [
		[
			KeyboardButton(text=city)
		]
	],
	resize_keyboard=True
	)

	await message.answer(f'Город {city} добавлен)', reply_markup=all_keyboard)
	await state.update_data(answer1=answer)

	await state.finish()


#Парсинг и последущий вывод погоды
@dp.message_handler()
async def get_weather(message: types.Message):

	code_to_smile = {

	'Clear': 'Ясно ☀️',
	'Clouds': 'Облачно ☁️',
	'Rain': 'Дождь 🌧',
	'Thunderstorm': 'Гроза ⛈',
	'Snow': 'Снег 🌨',
	'Mist': 'Туман 🌫'

	}

	try:
		r = requests.get(
			f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric'
			)
		data = r.json()

		city = data['name']
		cur_weather = data['main']['temp']

		weather_description = data['weather'][0]['main']
		if weather_description in code_to_smile:
			wd = code_to_smile[weather_description]
		else:
			wd = 'Выгляни в окно🙃'


		humidity = data['main']['humidity']
		pressure = data['main']['pressure']
		wind = data['wind']['speed']
		day_lenght = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

		await message.reply(	f'*** {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")} ***\n'
				f'Погода в городе: {city}\n\nТемпература: {cur_weather} C° {wd}\n\n'
				f'Влажность: {humidity} %\n\nДавление: {pressure} мм. рт. ст.\n\nСкорость ветра: {wind} м/с\n\nПродолжительность дня: {day_lenght}\n\n'
			)
			
	except:
		await message.reply('Мне кажется такого города нет)')


if __name__ == '__main__':
	executor.start_polling(dp)