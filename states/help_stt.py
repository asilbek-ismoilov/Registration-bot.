from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Help(StatesGroup):
    help = State()


# Define admin states
class AdminStates(StatesGroup):
    waiting_for_admin_message = State()
    waiting_for_reply_message = State()

# Function to create inline keyboard for reply
def create_inline_keyboard(user_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Javob berish",
        callback_data=f"reply:{user_id}"
    )


    return keyboard_builder.as_markup()

class Course(StatesGroup):
    name = State()
    description = State()

class Show(StatesGroup):
    name = State()