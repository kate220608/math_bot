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
            if update.message.reply_to_message.text == "Введите уравнение":
                if any(map(str.isdigit, text)) and any(map(lambda x: x.lower() == 'x', text)):
                    if '//' in text:
                        res = get_solution(text.replace('//', '/'))
                    elif '**' in text:
                        res = get_solution(text.replace('**', '^'))
                    else:
                        res = get_solution(text)
                    if res is not None:
                        await update.message.reply_text(res)
                    else:
                        await update.message.reply_text("Решения нет.")
                else:
                    await update.message.reply_text("Это не уравнение")
            elif update.message.reply_to_message.text == "Введите пример":
                if any(map(str.isdigit, text)) and any(map(lambda x: x in OPERATORS, text)):
                    if '√' in text:
                        await update.message.reply_text(float(text.replace('√', '')) ** 0.5)
                    else:
                        await update.message.reply_text(eval(text))
                else:
                    await update.message.reply_text('Это не пример')
        else:
            await update.message.reply_photo("Ответьте на сообщение", photo=open('img/how_to_send.jpg', 'rb'))

