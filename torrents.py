import telegram, webbrowser, os, time

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from variables import *

token=token_torrents
bot = telegram.Bot(token)

CHOOSING =range(3)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, Mrs. Grigorovsky!\nWelcome!")
    return CHOOSING

def download_on_id(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Приступаю к скачиванию")
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Id of torrent is {}'.format(text.lower()))
    url = 'https://rutracker.org/forum/dl.php?t=' + text
    webbrowser.get(chrome_path + " %s").open(url)
    time.sleep(3)
    os.chdir(downloads_path)
    file_name = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)[-1]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Вообщем, я скачал файл, он называется:\n' +
                                                                    file_name)
    download_file = downloads_path + "\\" + file_name
    os.startfile(download_file)

def path(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    os.chdir(downloads_path)
    print(os.listdir(os.getcwd()))
    file_name = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)[-1]
    print(file_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Вообщем, я скачал файл, он называется:\n' +
                                                                    file_name)
    # update.message.reply_text('Вообщем, я скачал файл, он называется:\n'
    #                           '{}'.formate(file_name))

def done(update, context):
    try:
        user_data = context.user_data
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_text("Okay, boomer")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Так-то все работает")

        user_data.clear()
        return ConversationHandler.END
    except Exception as exception:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Error: %s!\n\n" % exception)

try:
    proxy_kwargs
    updater = Updater(token, use_context=True, request_kwargs=proxy_kwargs)
except:
    updater = Updater(token, use_context=True)

def main():
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
                      ],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^\d*$'),
                                      download_on_id),
                       MessageHandler(Filters.regex('^path$'),
                                      path),
                       ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()
