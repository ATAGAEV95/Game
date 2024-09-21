import logging
import psycopg2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.bot_token import cesar_bot_token, password_postgres, host_postgres

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

en_alphabet = [chr(i) for i in range(65, 91)] + [chr(j) for j in range(97, 123)]
ru_alphabet = [chr(i) for i in range(1040, 1104)]

def cezar(text, k):
    result = ''
    for char in text:
        if char in en_alphabet:
            if char.isupper():
                result += en_alphabet[(en_alphabet.index(char) + k) % 26]
            else:
                result += en_alphabet[(en_alphabet.index(char.lower()) + k) % 26].lower()
        elif char in ru_alphabet:
            if char.isupper():
                result += ru_alphabet[(ru_alphabet.index(char) + k) % 32]
            else:
                result += ru_alphabet[(ru_alphabet.index(char.lower()) + k) % 32 + 32]
        else:
            result += char
    return result

def get_db_connection():
    return psycopg2.connect(
        dbname='postgres',
        user='atagaev',
        password=password_postgres,
        host=host_postgres,
        port='5432'
    )

def log_message(message_type, message_text, user_id=None, username=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO messages (message_type, message_text, user_id, username) VALUES (%s, %s, %s, %s)",
        (message_type, message_text, user_id, username)
    )
    connection.commit()
    cursor.close()
    connection.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Отправь текст и шаг сдвига в формате "текст ~ шаг".')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input_data = update.message.text.split('~')
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        log_message("Received", update.message.text, user_id, username)
        if len(input_data) != 2:
            await update.message.reply_text('Неверный формат. Используйте: "текст ~ шаг".')
            log_message("Sent", 'Неверный формат. Используйте: "текст ~ шаг".', user_id, username)
            return
        text, k = input_data[0].strip(), int(input_data[1].strip())
        if len(text) > 3000:
            await update.message.reply_text('Текст слишком длинный, максимальная длина - 3000 символов.')
            log_message("Sent", 'Текст слишком длинный, максимальная длина - 3000 символов.', user_id, username)
            return
        encrypted_text = cezar(text, k)
        await update.message.reply_text(encrypted_text)
        log_message("Sent", encrypted_text, user_id, username)
    except ValueError:
        await update.message.reply_text('Ошибка: убедитесь, что шаг - это число.')
        log_message("Sent", 'Ошибка: убедитесь, что шаг - это число.', user_id, username)


if __name__ == '__main__':
    app = ApplicationBuilder().token(cesar_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()