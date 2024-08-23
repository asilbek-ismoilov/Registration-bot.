from loader import dp, db, bot, ADMINS
from aiogram import F
import re
from states.register_stt import SingUp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboard_buttons.default.menu import tel, menu_button
from aiogram.types import CallbackQuery
from keyboard_buttons.inline import inline_val
from keyboard_buttons.default.menu import cours
from keyboard_buttons.inline.inline_val import reg_courses



# <-------------------------- Python qismi start ----------------------------------------------------------------------------->

@dp.message(F.text == "Python")
async def show_python_course_details(message: Message,state:FSMContext):
    await state.clear()
    await state.update_data(cours = "Python")
    python_course_info = """
📚 *Python Dasturlash Kursi*
📅 Boshlanish vaqti: 2024-09-01
⏳ Davomiyligi: 8 oy
💰 Narxi: 400,000 UZS oyiga

🔍 *Nimalarni o'rganasiz?*
- Python asoslari
- Ma'lumotlar tuzilmalari
- OOP (Object-Oriented Programming)
- Django framework yordamida web dasturlar yaratish
- Botlar yaratish va boshqa qiziqarli loyihalar

👨‍🏫 *Mentorlar:*
- Muhammad Aliyev (5 yillik tajriba)
- Nargiza Sodiqova (Python Data Science mutaxassisi)

📌 Batafsil ma'lumot uchun admin bilan bog'laning.

Agar kursga ro'yxatdan o'tmoqchi bo'lsangiz pastdagi tugmani bosing 👇👇👇
"""

    # Kurs haqida ma'lumot yuborish
    await message.answer(python_course_info, parse_mode="Markdown",reply_markup=reg_courses)

# <-------------------------- Python qismi finish ----------------------------------------------------------------------------->

# <-------------------------- SMM qismi start ----------------------------------------------------------------------------->

@dp.message(F.text == "SMM")
async def show_python_course_details(message: Message,state:FSMContext):
    await state.clear()
    await state.update_data(cours = "SMM")
    python_course_info = """
📚 *SMM Dasturlash Kursi*
📅 Boshlanish vaqti: 2024-09-01
⏳ Davomiyligi: 3 oy
💰 Narxi: 1,200,000 UZS

🔍 *Nimalarni o'rganasiz?*
- Python asoslari
- Ma'lumotlar tuzilmalari
- OOP (Object-Oriented Programming)
- Django framework yordamida web dasturlar yaratish
- Botlar yaratish va boshqa qiziqarli loyihalar

👨‍🏫 *Mentorlar:*
- Muhammad Aliyev (5 yillik tajriba)
- Nargiza Sodiqova (Python Data Science mutaxassisi)

📌 Batafsil ma'lumot uchun admin bilan bog'laning.

Agar kursga ro'yxatdan o'tmoqchi bo'lsangiz pastdagi tugmani bosing 👇👇👇
"""

    # Kurs haqida ma'lumot yuborish
    await message.answer(python_course_info, parse_mode="Markdown", reply_markup=reg_courses)


# <-------------------------- SMM qismi finish ----------------------------------------------------------------------------->

    
@dp.callback_query(F.data == "reg_cours")
async def reg_cours(callback:CallbackQuery,state:FSMContext):
    await callback.message.delete()
    await callback.message.answer("<b>Ismingizni kiriting</b> ✍", parse_mode='html', reply_markup=None)
    await state.set_state(SingUp.name)

# name
@dp.message(F.text, SingUp.name)
async def send_advert(message:Message,state:FSMContext):
    name = message.text
    if name.isalpha():
        await state.update_data(name = name)
        await message.answer("<b>Familiyani kiriting ✍</b>" , parse_mode='html')
        await state.set_state(SingUp.surname)
    else:
        await message.delete()
        await message.answer("<b>Ismingizni to'g'ri kiriting ❗️</b>", parse_mode='html')
        

@dp.message(SingUp.name)
async def name_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "<b>Ismingizni to'g'ri kiriting ❗️</b>", parse_mode='html')


# surname
@dp.message(F.text, SingUp.surname)
async def surname(message:Message, state:FSMContext):
    surname = message.text
    if surname.isalpha():
        await state.update_data(surname = surname)
        await message.answer("<b>☎️ Telefon raqamingizni kiriting ✍</b>", reply_markup=tel, parse_mode='html')
        await state.set_state(SingUp.tel)
    else:
        await message.delete()
        await message.answer("<b>Familiyani to'g'ri kiriting ❗️</b>", parse_mode='html')


@dp.message(SingUp.surname)
async def surname_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "<b>Familiyani to'g'ri kiriting ❗️</b>", parse_mode='html')


@dp.message(F.contact | F.text, SingUp.tel)
async def phone_number(message: Message, state: FSMContext):
    phone = message.text
    
    data = await state.get_data()

    name = data.get("name")
    surname = data.get("surname")
    cours = data.get("cours")
    
    if phone is None:
        phone = message.contact.phone_number
    
    if not phone.startswith("998"):
            phone = "+998" + phone

    # elif not phone.startswith("+998"):
    #     phone = "+998" + phone

    if re.fullmatch(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", phone):
        await state.update_data(phone=phone)
        f_text = f"<blockquote>Ma'lumotlaringiz to'g'rimi tekshiring ❗️❗️❗️</blockquote>\nKurs: {cours} \n<b>Ism-Familiya</b>: {name} {surname} \n<b>Tel</b>: {phone}"
        await message.answer(f_text, reply_markup=inline_val.confirmation, parse_mode='html')
    else:
        await message.delete()
        await message.answer(text= "Telefon raqamni to'g'ri kiriting ❗️ \n998 ham kiriting ❗️", parse_mode='html')



@dp.message(SingUp.tel)
async def phone_number_del(message:Message):
    await message.delete()
    await message.answer(text= "Telefon raqamni to'g'ri kiriting ❗️", parse_mode='html')
    await message.delete()


@dp.callback_query(F.data == "cancel")
async def cancel(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("<b>Menu</b>", parse_mode='html', reply_markup=menu_button)

@dp.callback_query(F.data == "change")
async def edit(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Qayta ro'yxatdan o'tish\n<b>Ismingizni kiriting</b> ✍", parse_mode='html', reply_markup=menu_button)


@dp.callback_query(F.data == "right")
async def right(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Siz muvaffaqiyatli ro'yxatdan o'tingiz 🎉, tez orada admin siz bilan bog'lanadi ✅\n<b>Menu</b>", reply_markup=menu_button , parse_mode='html')
    await callback.message.delete()

    data = await state.get_data()
    cours = data.get("cours")
    name = data.get("name")
    surname = data.get("surname")
    phone = data.get("phone")


    text = f"Yangi o'quvchi 👤\n<blockquote>Kurs: {cours} \n<b>Ism-Familiya</b>: {name} {surname} \n<b>Tel</b>: {phone}</blockquote>"
    await bot.send_message(ADMINS[0], text, parse_mode='html')

    # Foydalanuvchi ma'lumotlarini bazaga qo'shish
    full_name = f"{name} {surname}"
    db.add_user(telegram_id=callback.from_user.id, full_name=full_name, name=name, surname=surname, phone=phone)

    await state.clear()
