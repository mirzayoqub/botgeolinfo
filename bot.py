import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import config
from db import db

bot = telebot.TeleBot(config.token, parse_mode=None)


home = ReplyKeyboardMarkup(resize_keyboard=True)
home.add("⬅️back to home")

def markup():
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    markup.add(
        KeyboardButton("Uzbekcha"),
        KeyboardButton("Русский")
    )
    return markup

type_keyboard_ru = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
type_keyboard_ru.add('Жалоба', 'Предложение', "Оценка")
type_keyboard_ru.row('⬅️Назад')

type_keyboard_uz = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
type_keyboard_uz.add('Bildirgi', 'Maslahat', "Baholash")
type_keyboard_uz.row("⬅️Orqaga")


def get_menu(lang):
    db_name = db()
    name = db_name.get_name(lang=lang)
    return name

score = ReplyKeyboardMarkup()
score.row(InlineKeyboardButton('⭐️', callback_data=1))
score.row(InlineKeyboardButton('⭐️⭐️', callback_data=2))
score.row(InlineKeyboardButton('⭐️⭐️⭐️', callback_data=3))
score.row(InlineKeyboardButton('⭐️⭐️⭐️⭐️', callback_data=4))
score.row(InlineKeyboardButton('⭐️⭐️⭐️⭐️⭐️', callback_data=5))

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, f"Assalomu alaykum! Hush kelibsiz \nПривет! Я бот для обработки жалоб и предложений \n{message.from_user.first_name}",
                     reply_markup=markup())

@bot.message_handler(func=lambda message: message.text in ['Русский', "Uzbekcha"])
def select_language(message):
    if message.text == "Русский":
        bot.send_message(message.chat.id, "Выберите тип обращения:",
                         reply_markup=type_keyboard_ru)
        bot.register_next_step_handler(message, lambda feedback_type: next_step(message, feedback_type.text))
    elif message.text == "Uzbekcha":
        bot.send_message(message.chat.id, "Tanlang:",
                         reply_markup=type_keyboard_uz)
        bot.register_next_step_handler(message, lambda feedback_type: next_step(message, feedback_type.text))
    else:
        bot.send_message(message.chat.id, "Sorry")





def next_step(message, feedback):
    if message.text == 'Uzbekcha':
        if feedback in ['Bildirgi', 'Maslahat', "Baholash"]:
            bot.send_message(message.chat.id, "Tanlang:", reply_markup=get_menu(message.text))
            bot.register_next_step_handler(message, lambda next_step: department(message, feedback, next_step.text))
        elif feedback == '⬅️Orqaga':
            bot.send_message(message.chat.id, "⬅️Orqaga", reply_markup=markup())
        else:
            bot.send_message(message.chat.id, "Tugmaning tanlang", reply_markup=type_keyboard_uz)
    elif message.text == "Русский":
        if feedback in ['Жалоба', 'Предложение', "Оценка"]:
            bot.send_message(message.chat.id, "Выберай:", reply_markup=get_menu(message.text))
            bot.register_next_step_handler(message, lambda next_step: department(message, feedback, next_step.text))
        elif feedback == '⬅️Назад':
            bot.send_message(message.chat.id, "⬅️Назад", reply_markup=markup())
        else:
            bot.send_message(message.chat.id, "выберай:", reply_markup=type_keyboard_ru)
    else:
        bot.send_message(message.chat.id, "Sorry")



def department(message, feedback, department):
    if message.text == 'Uzbekcha':
        if department in ['fond', 'kadastr']:
            if feedback == "Baholash":
                bot.send_message(message.chat.id, "Baholang:", reply_markup=score)
                bot.register_next_step_handler(message, lambda next_step: callback_query(message, feedback, department, next_step.text))
            else:
                bot.send_message(message.chat.id, "Izoh qoldiring:", reply_markup=home)
                bot.register_next_step_handler(message, lambda next_step: send_file(message, feedback, department, next_step.text))
        elif department == '⬅️Orqaga':
            bot.send_message(message.chat.id, "⬅️Orqaga", reply_markup=type_keyboard_uz)
            select_language(message)
        else:
            bot.send_message(message.chat.id, "Tugmani tanlang", reply_markup=get_menu(message.text))
    elif message.text == "Русский":
        # mysql connect
        if department in ['Фонд', 'Кадастр']:
            if feedback == "Оценка":
                bot.send_message(message.chat.id, "Oценивайте:", reply_markup=score)
                bot.register_next_step_handler(message, lambda next_step: callback_query(message, feedback, department,next_step.text))
            else:
                bot.send_message(message.chat.id, "Оставить комментарий:", reply_markup=home)
                bot.register_next_step_handler(message, lambda next_step: send_file(message, feedback, department, next_step.text))
        elif department == '⬅️Назад':
            bot.send_message(message.chat.id, "⬅️Назад", reply_markup=type_keyboard_ru)
            select_language(message)
        else:
            bot.send_message(message.chat.id, "Выберай:", reply_markup=get_menu(message.text))
    else:
        bot.send_message(message.chat.id, "Sorry")


def send_file(message, feedback, department, file):
    if file == '⬅️back to home':
        if message.text == 'Uzbekcha':
            bot.send_message(message.chat.id, "⬅️Orqaga:", reply_markup=type_keyboard_uz)
            select_language(message)
        else:
            bot.send_message(message.chat.id, "⬅️Назад:", reply_markup=type_keyboard_ru)
            select_language(message)
    else:
        data = db()
        if message.text == 'Русский':
            data.save_db(message, feedback, department, file)
            bot.send_message(message.chat.id, "Спасибо")
            select_language(message)
        elif message.text == 'Uzbekcha':
            data.save_db(message, feedback, department, file)
            bot.send_message(message.chat.id, "Rahmat")
            select_language(message)
        else:
            bot.send_message(message.chat.id, "Opps sorry")


#
def callback_query(message, feedback, department, score):
    data_base = db()
    if message.text == 'Uzbekcha':
        data_base.save_score(department, int(len(score)/2))
        bot.send_message(message.chat.id, 'rahmat')
        select_language(message)
    else:
        data_base.save_score(department, int(len(score)/2))
        bot.send_message(message.chat.id, 'Спасибо')
        select_language(message)

bot.polling()