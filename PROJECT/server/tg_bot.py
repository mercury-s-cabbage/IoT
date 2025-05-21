import threading
import paho.mqtt.client as mqtt_client
import telebot
from telebot import types
import random
from t import t
from mqtt import  mqtt_loop
from tasks import tasks

current_data = "Нет данных"

my_token = t.get("BOT_API_TOKEN")
bot = telebot.TeleBot(my_token)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Регистрация")
    about_button = types.KeyboardButton("Об игре")
    action_button = types.KeyboardButton("Играть")
    try_button = types.KeyboardButton("Проверить")
    markup.add(start_button, action_button, try_button)
    bot.send_message(message.chat.id,
                     text=f"Привет, {message.from_user.first_name}!\nНачнем играть?",
                     reply_markup=markup)

@bot.message_handler(content_types=['text'])
def buttons(message):
    global current_data
    if message.text == "Регистрация":
        bot.send_message(message.chat.id, text="Укажите имя вашего героя")
    elif message.text == "Играть":
        bot.send_message(message.chat.id, text=f"{random.choice(tasks)}")
        # TODO: Доставать эти данные из БД
    elif message.text == "Проверить":
        bot.send_message(message.chat.id, text=f"Текущие данные устройства: {current_data}")
        #TODO: Доставать эти данные из БД
    elif message.text == "Об игре":
        bot.send_message(message.chat.id, text="Информация об игре")
    else:
        bot.send_message(message.chat.id, text="Я могу отвечать только на нажатие кнопок")

def bot_loop():
    bot.polling(none_stop=True)


mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
mqtt_thread.start()

bot_loop()
