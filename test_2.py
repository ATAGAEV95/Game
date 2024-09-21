from telegram.ext import Updater
import logging
from utils.bot_token import test_2_bot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = test_2_bot
# получаем экземпляр `Updater`
updater = Updater(token=TOKEN, use_context=True)
# получаем экземпляр `Dispatcher`
dispatcher = updater.dispatcher