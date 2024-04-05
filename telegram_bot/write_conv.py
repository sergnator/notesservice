from telegram.ext import CommandHandler, Application, MessageHandler, filters, ConversationHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, Update

buttons = ReplyKeyboardMarkup("Да", "Нет")


async def write_text(update: Update, context: CallbackContext):
    await update.message.reply_text('введите текст заметки')
    return 1


async def set_private(update: Update, context: CallbackContext):
    text = update.message.text
    await update.message.reply_text('сделать приватной записку', reply_markup=buttons)
    return 2
