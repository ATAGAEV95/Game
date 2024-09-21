from telegram.ext import Updater
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = '7890928323:AAGkIVlJS7BcHh5z-64nAwriYoHRjVoPx1w'
# получаем экземпляр `Updater`
updater = Updater(token=TOKEN, use_context=True)
# получаем экземпляр `Dispatcher`
dispatcher = updater.dispatcher