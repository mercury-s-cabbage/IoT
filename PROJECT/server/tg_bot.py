import threading
import paho.mqtt.client as mqtt_client
import telebot
from telebot import types
import random
from t import t
from mqtt import  mqtt_loop
import bd_interactions as bdi
import sqlite3
import hashlib
from logger_setup import setup_logger
import datetime

logger = setup_logger()

current_data = "Нет данных"
user_data = {}

my_token = t.get("BOT_API_TOKEN")
bot = telebot.TeleBot(my_token)

# Создаем панель с кнопками
@bot.message_handler(commands=['start'])
def start_message(message):
    logger.info(f"Received /start from chat_id={message.chat.id}, user={message.from_user.first_name}")
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
    logger.info(f"Button pressed: '{message.text}' by chat_id={message.chat.id}")
    global current_data
    if message.text == "Регистрация":
        msg = bot.send_message(message.chat.id, text="Укажите имя вашего героя")
        bot.register_next_step_handler(msg, get_hero_name)
    elif message.text == "Играть":
        level_id, answer, loose_text = send_random_level(message.chat.id)
        if answer is not None:
            bot.register_next_step_handler(message, lambda m: check_answer(m, level_id, answer, loose_text))
    elif message.text == "Правила":
        bot.send_message(message.chat.id, text="В этой игре вам предстоит проходить испытания в поисках"
                                               " правильной дороги. Нажмите 'Играть', а затем внимательно изучите"
                                               " уровень. В каждой строке есть лишь одна платформа, на которую может"
                                               " ступить ваше персонаж. Ваша задача - отправить в ответ на задание число"
                                               ", состоящее из номеров выбранных платформ, например, 1234. "
                                               "Мы сообщим, если ваш персонаж выживет :)")
    else:
        bot.send_message(message.chat.id, text="Я могу отвечать только на нажатие кнопок")

# --------------------------- Регистрация ----------------------------
def get_hero_name(message):
    chat_id = message.chat.id
    hero_name = message.text.strip()
    logger.debug(f"get_hero_name called: chat_id={chat_id}, hero_name='{hero_name}'")

    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users WHERE chat_id = ?", (chat_id,))
    users = cursor.fetchall()

    user = next((user for user in users if user[1] == hero_name), None)

    if user:
        user_data[chat_id] = {'name': hero_name, 'user_id': user[0]}
        bot.send_message(chat_id, f"Добро пожаловать, {hero_name}!")
        logger.info(f"User found: user_id={user[0]}, name={hero_name}")
    else:
        user_data[chat_id] = {'name': hero_name}
        msg = bot.send_message(chat_id, "Укажите номер устройства")
        bot.register_next_step_handler(msg, get_device_number)
        logger.info(f"New user registration started: chat_id={chat_id}")

    conn.close()

def get_device_number(message):
    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()
    chat_id = message.chat.id
    device_number = message.text.strip()
    name = user_data[chat_id]['name']
    logger.debug(f"get_device_number called: chat_id={chat_id}, device_number='{device_number}'")
    try:
        user_id = bdi.register_user(cursor, name, chat_id, device_number)
        conn.commit()
        bot.send_message(chat_id, f"Регистрация завершена! Добро пожаловать, {name}.")
        user_data[chat_id] = {'name': name, 'user_id': user_id}
        logger.info(f"User registered: user_id={user_id}, name={name}")
    except ValueError as e:
        bot.send_message(chat_id, str(e))
        msg = bot.send_message(chat_id, "Пожалуйста, введите номер устройства ещё раз")
        bot.register_next_step_handler(msg, get_device_number)
        logger.warning(f"Registration error for chat_id={chat_id}: {e}")
    conn.close()

# --------------------------- Игра ----------------------------
def send_random_level(chat_id):
    logger.info(f"send_random_level called for chat_id={chat_id}")
    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()

    user_info = user_data.get(chat_id)
    if user_info and 'user_id' in user_info:
        user_id = user_info['user_id']
        h = hashlib.new('sha256')
        client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION2,
            h.hexdigest()[:10]
        )
        client.publish("devices/01.001", user_id)
        logger.info(f"Published user_id={user_id} to MQTT topic 'devices/01.001'")
    else:
        bot.send_message(chat_id, "Пользователь не зарегистрирован.")
        logger.warning(f"User not registered: chat_id={chat_id}")
        conn.close()
        return None, None, None

    cursor.execute('''
        SELECT level_id FROM user_progress
        WHERE user_id = ? AND result = 1
    ''', (user_id,))
    passed_levels = {row[0] for row in cursor.fetchall()}

    cursor.execute('SELECT id FROM levels')
    all_levels = [row[0] for row in cursor.fetchall()]

    available_levels = [lvl for lvl in all_levels if lvl not in passed_levels]

    if not available_levels:
        bot.send_message(chat_id, "Вы успешно прошли все уровни! Поздравляем!")
        logger.info(f"All levels passed for user_id={user_id}")
        conn.close()
        return None, None, None

    level_id = random.choice(available_levels)

    cursor.execute('SELECT name, text, image_path, answer, loose_text FROM levels WHERE id = ?', (level_id,))
    level = cursor.fetchone()
    conn.close()

    if not level:
        bot.send_message(chat_id, "Ошибка при загрузке уровня.")
        logger.error(f"Error loading level id={level_id}")
        return None, None, None

    name, text, image_path, answer, loose_text = level

    bot.send_message(chat_id, f"<b>{name}</b>\n{text}", parse_mode='HTML')
    logger.info(f"Sent level '{name}' to chat_id={chat_id}")

    if image_path:
        try:
            with open(image_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            logger.info(f"Sent image for level '{name}'")
        except Exception as e:
            bot.send_message(chat_id, f"Не удалось загрузить изображение: {e}")
            logger.error(f"Failed to send image for level '{name}': {e}")

    return level_id, answer, loose_text

def check_answer(message, level_id, answer, loose_text):
    chat_id = message.chat.id
    user_answer = message.text.strip()
    logger.debug(f"check_answer called: chat_id={chat_id}, user_answer='{user_answer}', expected_answer='{answer}'")

    user_id = user_data[chat_id]['user_id']

    conn = sqlite3.connect('DungeonGame.db')
    cursor = conn.cursor()

    date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('SELECT data FROM data WHERE chat_id = ? ORDER BY id DESC LIMIT 1', (chat_id,))
    row = cursor.fetchone()
    device_answer = str(row[0]) if row else None
    logger.debug(f"Device answer from DB: {device_answer}")

    if user_answer == str(answer) or device_answer == str(answer):
        bot.send_message(chat_id, "Вы выжили и идёте дальше.")
        logger.info(f"Correct answer for chat_id={chat_id}")

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
            logger.info(f"All levels completed for chat_id={chat_id}")
    else:
        bot.send_message(chat_id, loose_text or "Неверный ответ. Игра окончена.")
        logger.info(f"Incorrect answer for chat_id={chat_id}")

        cursor.execute('''
            INSERT OR REPLACE INTO user_progress (user_id, level_id, result, date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, level_id, 0, date_str))
        conn.commit()

    conn.close()

# --------------------------- Запуск бота ----------------------------
def bot_loop():
    logger.info("Bot polling started")
    bot.polling(none_stop=True)

mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
mqtt_thread.start()
logger.info("MQTT thread started")

bot_loop()