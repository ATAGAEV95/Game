import telebot
from telebot import types

bot = telebot.TeleBot("7438499030:AAEXkd5sV-sND1eqy6m-IHMAX9JEftpztvk")

range_start = None
range_end = None

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    markup.add(item1)
    bot.send_message(message.chat.id, "Привет! Я бот для игры 'Загадай число'. Нажми 'Начать игру'. "
                                      "Затем введи начальное и конечное число, а я попытаюсь его угадать. "
                                      "Используй кнопки 'больше', 'меньше' или 'угадал' чтобы подсказывать мне.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Начать игру")
def start_game(message):
    global count
    count = 0
    bot.send_message(message.chat.id, "Введите начальное число:")
    bot.register_next_step_handler(message, get_start_number)

def get_start_number(message):
    global range_start
    try:
        start_number = int(message.text)
        range_start = start_number
        bot.send_message(message.chat.id, "Введите конечное число:")
        bot.register_next_step_handler(message, get_end_number, start_number)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите целое число.")
        bot.register_next_step_handler(message, get_start_number)

def get_end_number(message, start_number):
    global range_end
    try:
        end_number = int(message.text)
        range_end = end_number
        if end_number > start_number:
            guess_number(start_number, end_number, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Конечное число должно быть больше начального. Пожалуйста, введите корректные значения.")
            bot.register_next_step_handler(message, get_end_number, start_number)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите целое число.")
        bot.register_next_step_handler(message, get_end_number, start_number)

def guess_number(start, end, chat_id):
    guess = (start + end) // 2
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("угадал")
    item2 = types.KeyboardButton("меньше")
    item3 = types.KeyboardButton("больше")
    item5 = types.KeyboardButton("начать игру заново")
    markup.add(item1, item2, item3)
    markup.add(item5)
    user_response = bot.send_message(chat_id, f"Это число {guess} из диапазона чисел от {range_start} до {range_end}?", reply_markup=markup)
    bot.register_next_step_handler(user_response, process_response, start, end, guess, chat_id)

@bot.message_handler(func=lambda message: message.text == "начать игру заново")
def restart_game(message):
    global count
    count = 0
    bot.send_message(message.chat.id, "Введите начальное число:")
    bot.register_next_step_handler(message, get_start_number)

def process_response(message, start, end, guess, chat_id):
    user_response = message.text.lower()
    global count
    count += 1
    if user_response == "угадал":
        bot.send_message(chat_id, f"Ура! Число {guess} угадано. Попыток сделано {count}")
    elif user_response == "больше":
        start = guess + 1
        guess_number(start, end, chat_id)
    elif user_response == "меньше":
        end = guess - 1
        guess_number(start, end, chat_id)
    else:
        bot.send_message(chat_id, "Пожалуйста, введите 'больше', 'меньше' или 'угадал'.")
        bot.register_next_step_handler(message, process_response, start, end, guess, chat_id)

bot.infinity_polling()