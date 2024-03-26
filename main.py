import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup
from solution import get_solution
from data import db_session
from data.users import User
from work_with_db import add_user, delete_user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


start_reply_keyboard = [['/help', '/ask_sol']]
start_markup = ReplyKeyboardMarkup(start_reply_keyboard, one_time_keyboard=True)

sol_reply_keyboard = [['уравнение', 'пример']]
sol_markup = ReplyKeyboardMarkup(sol_reply_keyboard, one_time_keyboard=True)


async def start(update, context):
    user = update.effective_user
    greet_text = add_user(user.id, user.name)
    await update.message.reply_html(
        f"Привет, {user.mention_html()}!\n{greet_text}\nВыберите "
                                    "дальнейшую команду:", reply_markup=start_markup
    )


async def restart(update, context):
    delete_user(update.effective_user.id)
    await start(update, context)


async def help(update, context):
    sign_list = ['+ сложение', '- вычетание', '* умнoжение', '/ деление', '// деление нацело',
                 '** возведение в степень',
                 '% деление с остатком', '√ корень', '= равно']
    await update.message.reply_text(f"Знаки:\n" + '\n'.join(sign_list))


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


def main():
    db_session.global_init("db/telegram_bot.db")
    application = Application.builder().token("6395598122:AAHBaVYqltJw1PKsKm9lqALSZjppTAckRUo").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('restart', restart))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('ask_sol', ask_sol))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))
    application.run_polling()


if __name__ == '__main__':
    main()
