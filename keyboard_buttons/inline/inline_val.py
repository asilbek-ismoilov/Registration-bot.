from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

reg_courses = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text= "📋 Kursga yozilish", callback_data="reg_cours")]
    ]
)

confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text= "Bekor qilish ❌", callback_data="cancel"), InlineKeyboardButton(text= "Tasdiqlash ✅", callback_data="right")]
    ]
)

add_course = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Qo'shish ✅", callback_data="add course"),],
    ]
)

del_course = InlineKeyboardMarkup(
    inline_keyboard=[       
        [InlineKeyboardButton(text="O'chirish 🗑", callback_data="delete course")]
    ]
)