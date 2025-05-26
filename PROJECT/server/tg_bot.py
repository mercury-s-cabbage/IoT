import threading
import paho.mqtt.client as mqtt_client
import telebot
from telebot import types
import random
from t import t
from mqtt import  mqtt_loop
import bd_interactions as bdi
import sqlite3

current_data = "Нет данных"
user_data = {}

my_token = t.get("BOT_API_TOKEN")
bot = telebot.TeleBot(my_token)

# Создаем панель с кнопками
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Регистрация")
    about_button = types.KeyboardButton("Правила")
    action_button = types.KeyboardButton("Играть")
    markup.add(start_button, action_button, about_button)
    bot.send_message(message.chat.id,
                     text=f"Привет, {message.from_user.first_name}!\nНачнем играть?",
                     reply_markup=markup)

# Принимаем нажатия на кнопки
@bot.message_handler(content_types=['text'])
def buttons(message):
    global current_data
    if message.text == "Регистрация":
        msg = bot.send_message(message.chat.id, text="Укажите имя вашего героя")
        bot.register_next_step_handler(msg, get_hero_name)
    elif message.text == "Играть":
        level_id, answer, loose_text = send_random_level(message.chat.id)
        if answer is not None:
            bot.register_next_step_handler(message, lambda m: check_answer(m, level_id, answer, loose_text))

    elif message.text == "Об игре":
        bot.send_message(message.chat.id, text="Информация об игре")
    else:
        bot.send_message(message.chat.id, text="Я могу отвечать только на нажатие кнопок")

# --------------------------- Регистрация ----------------------------
def get_hero_name(message):
    chat_id = message.chat.id
    hero_name = message.text.strip()

    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()

    # Получаем id и имена пользователей с таким chat_id
    cursor.execute("SELECT id, name FROM users WHERE chat_id = ?", (chat_id,))
    users = cursor.fetchall()

    # Пытаемся найти пользователя с таким именем
    user = next((user for user in users if user[1] == hero_name), None)

    if user:
        # Пользователь найден
        user_data[chat_id] = {'name': hero_name, 'user_id': user[0]}
        bot.send_message(chat_id, f"Добро пожаловать, {hero_name}!")
    else:
        # Пользователь не найден — продолжаем регистрацию
        user_data[chat_id] = {'name': hero_name}
        msg = bot.send_message(chat_id, "Укажите номер устройства")
        bot.register_next_step_handler(msg, get_device_number)

    conn.close()

def get_device_number(message):
    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()
    chat_id = message.chat.id
    device_number = message.text.strip()
    name = user_data[chat_id]['name']
    try:
        user_id = bdi.register_user(cursor, name, chat_id, device_number, )
        conn.commit()
        bot.send_message(chat_id, f"Регистрация завершена! Добро пожаловать, {name}.")
        user_data[chat_id] = {'name': name, 'user_id': user_id}
    except ValueError as e:
        bot.send_message(chat_id, str(e))
        msg = bot.send_message(chat_id, "Пожалуйста, введите номер устройства ещё раз")
        bot.register_next_step_handler(msg, get_device_number)

# --------------------------- Игра ----------------------------
def send_random_level(chat_id):
    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()

    user_info = user_data.get(chat_id)
    #print(user_info)
    if user_info and 'user_id' in user_info:
        user_id = user_info['user_id']
        #TODO: отправляем боту топик, на который публиковать инфу
    else:
        bot.send_message(chat_id, "Пользователь не зарегистрирован.")
        conn.close()
        return None, None, None

    cursor.execute('''
        SELECT level_id FROM user_progress
        WHERE user_id = ? AND result = 1
    ''', (user_id,))
    passed_levels = {row[0] for row in cursor.fetchall()}

    # Получаем все уровни, исключая успешно пройденные
    cursor.execute('SELECT id FROM levels')
    all_levels = [row[0] for row in cursor.fetchall()]

    # Фильтруем уровни, которые пользователь ещё не прошёл или провалил
    available_levels = [lvl for lvl in all_levels if lvl not in passed_levels]

    if not available_levels:
        bot.send_message(chat_id, "Вы успешно прошли все уровни! Поздравляем!")
        conn.close()
        return None, None, None

    # Выбираем случайный уровень из доступных
    level_id = random.choice(available_levels)

    cursor.execute('SELECT name, text, image_path, answer, loose_text FROM levels WHERE id = ?', (level_id,))
    level = cursor.fetchone()
    conn.close()

    if not level:
        bot.send_message(chat_id, "Ошибка при загрузке уровня.")
        return None, None, None

    name, text, image_path, answer, loose_text = level

    bot.send_message(chat_id, f"<b>{name}</b>", parse_mode='HTML')
    bot.send_message(chat_id, text)

    if image_path:
        try:
            with open(image_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
        except Exception as e:
            bot.send_message(chat_id, f"Не удалось загрузить изображение: {e}")

    return level_id, answer, loose_text


import datetime

def check_answer(message, level_id, answer, loose_text):
    chat_id = message.chat.id
    user_answer = message.text.strip()

    user_id = user_data[chat_id]['user_id']
    #print(user_id)

    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()

    date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('SELECT data FROM data WHERE chat_id = ? ORDER BY id DESC LIMIT 1', (chat_id,))
    row = cursor.fetchone()
    device_answer = str(row[0]) if row else None
    print(device_answer)

    if user_answer == str(answer) or device_answer == str(answer):
        bot.send_message(chat_id, "Правильно! Переходим к следующему уровню.")

        cursor.execute('''
            INSERT OR REPLACE INTO user_progress (user_id, level_id, result, date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, level_id, 1, date_str))
        conn.commit()

        next_level_id, new_answer, new_loose_text = send_random_level(chat_id)
        if new_answer is not None:
            bot.register_next_step_handler(message, lambda m: check_answer(m, next_level_id, new_answer, new_loose_text))
        else:
            bot.send_message(chat_id, "Уровни закончились. Поздравляем!")
    else:
        bot.send_message(chat_id, loose_text or "Неверный ответ. Игра окончена.")

        cursor.execute('''
            INSERT OR REPLACE INTO user_progress (user_id, level_id, result, date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, level_id, 0, date_str))
        conn.commit()

    conn.close()

# --------------------------- Запуск бота ----------------------------
def bot_loop():
    bot.polling(none_stop=True)


mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
mqtt_thread.start()

bot_loop()
