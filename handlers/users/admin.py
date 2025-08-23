import time 
from aiogram import F
from states.reklama import Adverts
from aiogram.filters import Command
from loader import bot,db,dp,ADMINS
from states.help_stt import Course, Show
from aiogram.fsm.context import FSMContext
from filters.admin import IsBotAdminFilter
from keyboard_buttons.default import admin_keyboard
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboard_buttons.inline.inline_val import add_course, del_course


@dp.message(F.text == "Ortga 🔙", IsBotAdminFilter(ADMINS))
async def exit(message: Message):
    await message.answer("Menu", reply_markup=admin_keyboard.admin_button)

@dp.message(Command("admin"), IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni", IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish", IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


@dp.message(F.text == "Kurslar ro'yxati", IsBotAdminFilter(ADMINS))
async def courses(message: Message, state: FSMContext):
    await message.answer(text="Kurslarni boshqarish", reply_markup=add_course)

    await message.answer(
        text="Kurslar :", 
        reply_markup=admin_keyboard.course_keyboard()
    )
    await state.set_state(Show.name)

@dp.message(F.text, Show.name, IsBotAdminFilter(ADMINS))  
async def course_edit(message: Message, state: FSMContext):
    course_name = message.text
    await state.update_data(course_name = course_name)

    courses  = db.get_courses(f"{course_name}") 

    if not courses:
        await message.answer("Kechirasiz, bunday nomdagi kompyuter topilmadi.")
        return

    name, description = courses[0]  
    text = f"{description}" 

    await message.answer(text, reply_markup=del_course)


@dp.callback_query(F.data == "add course", IsBotAdminFilter(ADMINS))
async def add_courses(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("<b>Kurs nomini kiriting</b> ✍", parse_mode='html', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Course.name)


@dp.message(F.text, Course.name)
async def course_name(message:Message,state:FSMContext):
    name = message.text
    await state.update_data(name = name)
    await message.answer("<b>Kurs haqidagi matni kiriting ✍</b>" , parse_mode='html')
    await state.set_state(Course.description)

@dp.message(F.text, Course.description)
async def course_description(message:Message,state:FSMContext):
    description = message.text
    data = await state.get_data()

    name = data.get("name")

    db.add_course(name=name, description=description)
    await state.clear()
    await message.answer("Muvaffaqiyatli qo'shildi ✅")


@dp.callback_query(F.data == "delete course", IsBotAdminFilter(ADMINS))
async def add_courses(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    data = await state.get_data()
    course_name = data.get("course_name")

    db.delete_courses(course_name)
    text = f"<blockquote>{course_name} o'chirildi 🎉</blockquote>"

    for admin in ADMINS:
        await bot.send_message(chat_id=admin,text=text, parse_mode="HTML")

    await state.clear()
    