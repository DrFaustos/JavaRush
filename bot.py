from email.policy import default
from types import NoneType

from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode = 'main'
    text = load_message('main')
    await send_photo(update, context, 'main')
    await send_text(update, context, text)

async def gpt(update, context):
    dialog.mode= 'gpt'
    text = load_message('gpt')
    await send_photo(update, context, 'gpt')
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    answer = await chatgpt.send_question('Напиши четкий и короткий ответ на следующий вопрос:', text)
    await send_text(update, context, answer)

# тут будем писать наш код :)
async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, '*Привет*')
        await send_text(update, context, '_Как дела?_')
        await send_text(update, context, 'Вы написали '+ update.message.text)
        await send_photo(update,context, 'avatar_main')
        await send_text_buttons(update, context, 'Запустить процесс?', {
            'start':'Запустить',
            'stop':'Остановить'
    } )

async def hello_button(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, 'Процесс запущен')
    else:
        await send_text(update, context, 'Процесс остановлен')


dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token='gpt:6iWpGTIVtrvZB0KTFlGqJFkblB3Tjikl0aobFUM6zUmVCkXU')


app = ApplicationBuilder().token("7676179726:AAEzXm-UJFumBkOJT1HYLX5q9W2QOiLzYsc").build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
