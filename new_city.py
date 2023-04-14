from aiogram.dispatcher.filters.state import StatesGroup, State

#Состояние запроса города
class Ask(StatesGroup):
    Q1 = State()