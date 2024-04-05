from telegram.ext import CommandHandler, Application, MessageHandler, filters, ConversationHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, Update

from Constans import *

users = dict()

markup = ReplyKeyboardMarkup(["/write", "/read", "/edit", "delete"])

async def help_message(update: Update, context: CallbackContext):
    await update.message.reply_text("Используйте кнопки, так удобнее!")


async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in users.keys():
        await update.message.reply_text(
            "Я с вами ещё не знаком, войдите в свой аккаунт, просто введите имя и пароль через пробел")
        return 1
    else:
        await update.message.reply_text(
            f"с возвращением, {users[user_id][0]}")


async def login(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    users[user_id] = update.message.text.split()
    await update.message.reply_text(f"Приятно познакомится {users[user_id][0]}")
    return ConversationHandler.END


async def stop(update: Update, context: CallbackContext):
    return ConversationHandler.END


def main():
    application = Application.builder().token(TOKEN_BOT).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, help_message)
    conv_handler_login = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, login)],
        },
        fallbacks=[CommandHandler('stop', stop)]

    )

    application.add_handler(conv_handler_login)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
