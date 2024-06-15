from telebot import TeleBot, types
from models import get_user
import sqlite3
from pdf_generator import send_pdf
from werkzeug.security import generate_password_hash, check_password_hash

button = types.InlineKeyboardMarkup()
button.add(types.InlineKeyboardButton(text='привіт', callback_data='button1'))
button.add(types.InlineKeyboardButton(text='ти', callback_data='button2'))

markup2 = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Button 1')
itembtn2 = types.KeyboardButton('Button 2')
markup2.add(itembtn1, itembtn2)


def telegram_bot():
    token = "7125954288:AAHuEUOPeZ_Ug_LnagHH6DSJqKxwidl_cA8"
    bot = TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.reply_to(message, "Ви натиснули '/start'! ", reply_markup=button)

    @bot.message_handler(commands=["help"])
    def help_btn(message):
        bot.reply_to(message, "Ви натиснули '/help'! ", reply_markup=markup2)

    @bot.message_handler(commands=["info"])
    def info_command(message):
        parts = message.text.split(' ')
        if len(parts) == 3:
            command, username, password = parts
            user_info = get_user(username, password)
            if user_info:
                bot.reply_to(message, f"👤 Інформація про користувача:\n"
                                      f"- Ім'я користувача: {user_info[1]}\n"
                                      f"- Улюблене аніме: {user_info[3]}\n"
                                      f"- Улюблений фільм: {user_info[4]}")
            else:
                bot.reply_to(message, "Користувач з таким ім'ям та паролем не знайдений.")
        else:
            bot.reply_to(message, "Неправильний формат команди. Використовуйте /info ім'я пароль.")

    @bot.message_handler(commands=["sendpdf"])
    def send_pdf_command(message):
        chat_id = message.chat.id
        username = message.text.split(" ")[1].strip()

        send_pdf(bot, chat_id, username)

    @bot.message_handler(commands=['register'])
    def register_telegram(message):
        parts = message.text.split(' ')
        if len(parts) == 4:
            command, username, password, anime = parts
            response = register_user(username, password, anime)
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Неправильний формат команди. Використовуйте /register ім'я пароль аніме")

    @bot.message_handler(content_types=["text"])
    def text_message(message):
        if "привіт" in message.text.lower():
            bot.reply_to(message, "Привіт! ")

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'button1':
            bot.answer_callback_query(call.id, "Привіт! Як справи?")
        elif call.data == 'button2':
            bot.answer_callback_query(call.id, "Привіт, ти як?")

    def register_user(username, password, anime):
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password, anime) VALUES (?, ?, ?)',
                           (username, hashed_password, anime))
            conn.commit()
            return f"Пользователь {username} успішно зареєстрований."
        except sqlite3.IntegrityError:
            return "Користувач із таким ім'ям вже існує."

    bot.polling()
