from aiogram.fsm.state import State, StatesGroup

class SingUp(StatesGroup):
    name = State()
    surname = State()
    tel = State()

class Cours(StatesGroup):
    cours = State()
    descripton = State()
