import telebot
from t import t
from telebot import types
from tasks import tasks
import random

my_token = t.get('BOT_API_TOKEN')
bot = telebot.TeleBot(my_token)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Регистрация")
    about_button = types.KeyboardButton("Об игре")
    action_button = types.KeyboardButton("Играть")
    markup.add(start_button, action_button, about_button)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}"
                    " \nНачнем играть?".format(message.from_user),
                     reply_markup=markup)
@bot.message_handler(content_types=['text'])
def buttons(message):
    if (message.text == "Регистрация"):
        bot.send_message(message.chat.id, text="Укажите имя вашего героя")
    elif (message.text == "Играть"):
        bot.send_message(message.chat.id, text=f"{random.choice(tasks)}")
    elif (message.text == "Об игре"):
        bot.send_message(message.chat.id, text=f"Информация об игре")
    else:
        bot.send_message(message.chat.id, text="Я могу отвечать только на нажатие кнопок")

bot.polling(none_stop=True, interval=0)