import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from solution import get_solution
from data import db_session
from work_with_db import add_user, delete_user, last_example_from_user, last_equation_from_user
from work_with_files import open_equation, open_example

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

start_reply_keyboard = [['/help', '/ask_sol']]
start_markup = ReplyKeyboardMarkup(start_reply_keyboard, one_time_keyboard=True)

sol_reply_keyboard = [['уравнение', 'пример']]
sol_markup = ReplyKeyboardMarkup(sol_reply_keyboard, one_time_keyboard=True)

yes_or_no_keyboard = [['да', 'нет']]
yes_or_no_markup = ReplyKeyboardMarkup(yes_or_no_keyboard, one_time_keyboard=True)


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
    return 1


async def stop(update, context):
    await update.message.reply_text('До скорых встреч!')


async def example_or_equation(update, context):
    if update.message.text == "пример":
        last_example = last_example_from_user(update.effective_user.id)
        if last_example:
            await update.message.reply_html(
                f"В прошлый раз у вас вызвали затруднения <b>{last_example[0]}</b> примеры.\nПотренируемся?",
                reply_markup=yes_or_no_markup)
            return 2
        else:
            await update.message.reply_text("Введите пример")
            return 3

    if update.message.text == 'уравнение':
        last_equation = last_equation_from_user(update.effective_user.id)
        if last_equation:
            await update.message.reply_html(
                f"В прошлый раз у вас вызвали затруднения <b>{last_equation[0]}</b> уравнения.\nПотренируемся?",
                reply_markup=yes_or_no_markup)
            return 4
        else:
            await update.message.reply_text("Введите уравнение")
            return 5


async def example_training(update, context):
    if update.message.text == 'да':
        last_example = last_example_from_user(update.effective_user.id)
        try:
            await update.message.reply_text(open_example(last_example[1]))
        finally:
            return ConversationHandler.END
    else:
        await update.message.reply_text("Хорошо!\nВведите пример")
        return 3


async def example_get_sol(update, context):
    await update.message.reply_text(get_solution(update.message.text, 'пример',
                                                 update.effective_user.id))
    return ConversationHandler.END


async def equation_training(update, context):
    if update.message.text == 'да':
        last_equation = last_equation_from_user(update.effective_user.id)
        try:
            await update.message.reply_text(open_equation(last_equation[1]))
        finally:
            return ConversationHandler.END
    else:
        await update.message.reply_text("Хорошо!\nВведите уравнение")
        return 5


async def equation_get_sol(update, context):
    await update.message.reply_text(get_solution(update.message.text, 'уравнение',
                                                 update.effective_user.id))
    return ConversationHandler.END


def main():
    db_session.global_init("db/telegram_bot.db")
    application = Application.builder().token("6395598122:AAHBaVYqltJw1PKsKm9lqALSZjppTAckRUo").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('restart', restart))
    application.add_handler(CommandHandler('help', help))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('ask_sol', ask_sol)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, example_or_equation)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, example_training)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, example_get_sol)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, equation_training)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, equation_get_sol)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
