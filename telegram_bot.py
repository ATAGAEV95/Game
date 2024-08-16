from telebot import TeleBot
from telebot import types
import random

TOKEN = '6485989521:AAHyr3-YbhSJIe5FAdKehT_GrNXFo5G2tqY'

bot = TeleBot(TOKEN)

user_data = {}

class User:
    def __init__(self):
        self.state = 'START'
        self.a = None
        self.b = None
        self.x = None
        self.count = 0

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Окончить игру")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Привет! Я бот по игре «Угадай число». Сначала вы задаёте диапазон чисел, по которому будет сгенерировано число, а затем вы его отгадываете. "
    "После каждой попытки будет подсказка. "                 
    "Нажмите кнопку ниже, чтобы начать игру.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() == 'окончить игру')
def end_game(message):
    id = message.chat.id
    if id in user_data:
        user = user_data[id]
        user.state = 'START'
        user.a = None
        user.b = None
        user.x = None
        user.count = 0
        bot.reply_to(message, 'Игра окончена. Нажмите "Начать игру", чтобы начать заново.')

@bot.message_handler(func=lambda message: True)
def start_game(message):
    id = message.chat.id
    if id not in user_data:
        user_data[id] = User()
    user = user_data[id]
    text = message.text.lower()
    if text == 'начать игру':
        user.state = 'A'
        user.a = None
        user.b = None
        user.x = None
        user.count = 0
        bot.reply_to(message, 'Введите начальное число: ')
    elif user.state == 'A':
        try:
            user.a = int(text)
            user.state = 'B'
            bot.reply_to(message, 'Введите конечное число: ')
        except ValueError:
            bot.reply_to(message, 'Введите целое число')
    elif user.state == 'B':
        try:
            user.b = int(text)
            if user.b <= user.a:
                bot.reply_to(message, 'Конечное число должно быть больше начального числа. Введите конечное число заново: ')
            else:
                user.x = random.randint(user.a, user.b)
                user.state = 'GAME'
                bot.reply_to(message, f'Введите число от {user.a} до {user.b}: ')
        except ValueError:
            bot.reply_to(message, 'Введите целое число')
    elif user.state == 'GAME':
        try:
            y = int(text)
            if y < user.a or y > user.b:
                bot.reply_to(message, f'Введите число от {user.a} до {user.b}: ')
            else:
                user.count += 1
                if y == user.x:
                    bot.reply_to(message, f'Поздравляю, из диапозона чисел  от {user.a} до {user.b} вы угадали: {user.x}\nПопыток было сделано: {user.count}\nНачнем заново!')
                    user.state = 'START'
                    user.a = None
                    user.b = None
                    user.x = None
                    user.count = 0
                else:
                    bot.reply_to(message, 'Неверно, правильное число больше' if user.x > y else 'Неверно, правильное число меньше')
        except ValueError:
            bot.reply_to(message, 'Введите целое число')

bot.infinity_polling()