from telebot import TeleBot
from telebot import types
import random
from utils.bot_token import guess_bot_token

bot = TeleBot(guess_bot_token)

a, b, x, count = None, None, None, 0

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    markup.add(item1)
    bot.send_message(message.chat.id, "Привет! Я ваш бот. Нажмите кнопку ниже, чтобы начать игру.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global a, b, x, count
    text = message.text.lower()
    bot.reply_to(message, 'Введите начальное число: ')
    try:
        a = int(text)
        bot.reply_to(message, 'Введите конечное число: ')
    except ValueError:
        bot.reply_to(message, 'Введите число')
    try:
        b = int(text)
        while b <= a:
            bot.reply_to(message, 'Конечное число должно быть больше начального числа. Введите конечное число заново: ')
            b = int(text)
        x = random.randint(a, b)
        bot.reply_to(message, f'Введите число от {a} до {b}: ')
    except ValueError:
        bot.reply_to(message, 'Введите число')
    try:
        y = int(text)
        count += 1
        if y == x:
            bot.reply_to(message, f'Поздравляю, вы угадали: {x}\nПопыток было сделано: {count}\nНачнем заново!')
            a, b, x, count = None, None, None, 0
        else:
            bot.reply_to(message, 'Неверно, это число больше' if x > y else 'Неверно, это число меньше')
    except ValueError:
        bot.reply_to(message, 'Введите число')

bot.infinity_polling()