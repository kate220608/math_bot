from telebot.types import ReplyKeyboardMarkup

start_reply_keyboard = [['/help', '/ask_sol']]
start_markup = ReplyKeyboardMarkup(start_reply_keyboard, one_time_keyboard=True)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я бот, помогающий решать математические задачи.\n Выберите "
                                    "дальнейшую команду:", reply_markup=start_markup
    )


async def help(update, context):
    sign_list = ['+ сложение', '- вычетание', '* умнoжение', '/ деление', '// деление нацело',
                 '** возведение в степень',
                 '% деление с остатком', '√ корень', '= равно']
    await update.message.reply_text(f"Знаки:\n" + '\n'.join(sign_list))