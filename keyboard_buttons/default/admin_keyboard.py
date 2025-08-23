from loader import db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilar soni"),
            KeyboardButton(text="Reklama yuborish"),
        ],
        [
            KeyboardButton(text="Kurslar ro'yxati"),
            KeyboardButton(text="Manzil"),
        ]
        
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)

def get_course_keyboard():
    courses = [row[0] for row in db.all_course_name()]
    
    builder = ReplyKeyboardBuilder()
    
    for course in courses:
        builder.add(KeyboardButton(text=course))
    
    builder.add(KeyboardButton(text="Orqaga 🔙"))
    builder.adjust(3)
    
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Kursni tanlang...")

def course_keyboard():
    courses = [row[0] for row in db.all_course_name()]
    
    builder = ReplyKeyboardBuilder()
    
    for course in courses:
        builder.add(KeyboardButton(text=course))
    
    builder.add(KeyboardButton(text="Ortga 🔙"))
    builder.adjust(3)
    
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Kursni tanlang...")