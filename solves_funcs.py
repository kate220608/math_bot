from telebot.types import ReplyKeyboardMarkup
from solution import get_solution

OPERATORS = ['=', '-', '%', '+', '/', '^', '*', '√']


sol_reply_keyboard = [['уравнение', 'пример']]
sol_markup = ReplyKeyboardMarkup(sol_reply_keyboard, one_time_keyboard=True)


async def ask_sol(update, context):
    await update.message.reply_text('Выберите вид', reply_markup=sol_markup)


async def messages(update, context):
    text = update.message.text
    if text == "пример":
        await update.message.reply_text("Введите пример")
    elif text == "уравнение":
        await update.message.reply_text("Введите уравнение")
    else:
        if update.message.reply_to_message:
            await update.message.reply_text(get_solution(text, update.message.reply_to_message.text))
        else:
            await update.message.reply_photo(photo=open('img/how_to_send.jpg', 'rb'))



