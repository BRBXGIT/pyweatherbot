#Тестовый код парсера погоды, вшит в бота

import requests
from config import token
import datetime

def get_weather(city, token):

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
			f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric'
			)
		data = r.json()

		city = data['name']
		cur_weather = data['main']['temp']

		weather_description = data['weather'][0]['main']
		if weather_description in code_to_smile:
			wd = code_to_smile[weather_description]
		else:
			wd = 'Выгляни в окно'


		humidity = data['main']['humidity']
		pressure = data['main']['pressure']
		wind = data['wind']['speed']
		day_lenght = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

		print(	f'***{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}***\n'
				f'Погода в городе: {city}\nТемпература: {cur_weather} C° {wd}\n'
				f'Влажность: {humidity} %\nДавление: {pressure} мм столба\nСкорость ветра: {wind} м/\nПродолжительность дня: {day_lenght}'

			)

	except Exception as ex:
		print(ex)
		print('Проверьте название города')



def main():
	city = input('Введите город: ')
	get_weather(city, token)


if __name__ == '__main__':
	main()