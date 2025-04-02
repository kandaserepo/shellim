from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import string
import requests
from cryptography.fernet import Fernet
from pytz import timezone
tz = timezone('UTC')  # or 'Europe/Moscow' etc.
# Токен вашего бота
BOT_TOKEN = "8052337028:AAFM-AAP_1yg970RJR8p9l1TWReiZKvZ1Dw"

# URL сервера для регистрации
SERVER_URL = "https://shellflask.cloudpub.ru/register"

application = (
    Application.builder()
    .token(BOT_TOKEN)
    .arbitrary_callback_data(True)
    .post_init(lambda app: app.job_queue.scheduler.configure(timezone=tz))
    .build()
)
# Initialize Fernet key
try:
    with open("server_key.key", "rb") as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
except (FileNotFoundError, ValueError):
    key = Fernet.generate_key()
    with open("server_key.key", "wb") as key_file:
        key_file.write(key)
    cipher_suite = Fernet(key)



def generate_random_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sentence = "I love programming in Python"
    words = sentence.split()
    random.shuffle(words)
    context.user_data["correct"] = sentence
    await update.message.reply_text(
        "Welcome! Arrange these words correctly:\n" +
        " ".join(words)
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    correct = context.user_data.get("correct")

    if user_answer.strip() == correct:
        user_id = random.randint(1000, 9999)
        password = generate_random_password()

        try:
            response = requests.post(
                SERVER_URL,
                json={"user_id": user_id, "password": password}
            )
            if response.status_code == 200:
                await update.message.reply_text(
                    f"✅ Registered!\nID: {user_id}\nPassword: {password}"
                )
            else:
                await update.message.reply_text("❌ Registration failed")
        except requests.RequestException:
            await update.message.reply_text("⚠️ Server unavailable")
    else:
        await update.message.reply_text("❌ Incorrect. Try /start again")


def main():
    # Explicitly set timezone
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()