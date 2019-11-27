import telegram, smtplib, os, yaml, random

from datetime import datetime
from telegram.ext import Updater, CommandHandler,  MessageHandler, Filters, ConversationHandler
from variables import *

bot = telegram.Bot(token)
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, Mr. and Mrs. Grigorovsky.\n"
                                                                    "How is your day going?")
    return CHOOSING

def vasilich(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Время сдавать показатели воды?\n'
                                                                    'Пришли показатели через /vodichka '
                                                                    'проверочный код, значение холодной '
                                                                    'и горячей воды через пробелы.')

def vodichka(update, context):
    if len(context.args) == 3:
        secure_code = context.args[0]
        cold_water = context.args[1]
        hot_water = context.args[2]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Твой проверочный код: %s\n'
                                      'Твои показания холодной воды: %s\n'
                                      'Твои показания горячей воды: %s\n' %(secure_code, cold_water, hot_water))

        if secure_code == our_code:
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Письмо было отослано на ' +
                                              ', '.join(sent_to) + ' ящики от ' + datetime.now().strftime("%m/%d/%Y"))

                sent_from = gmail_user
                sent_subject = "Показания воды за" + datetime.now().strftime("%m/%d/%Y")
                email_body = ("Привет, Пишет тебе бот\n"
                             "Показания холодной воды: %s\n"
                             "Показания холодной воды: %s\n" % (cold_water, hot_water)
                             )

                sent_body = '\r\n'.join(['To: %s' % sent_to,
                                    'From: %s' % sent_from,
                                    'Subject: %s' % sent_subject,
                                    '',
                                    email_body])

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_app_password)
                server.sendmail(sent_from, sent_to, sent_body.encode('utf-8'))
                server.close()
            except Exception as exception:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Error: %s!\n\n" % exception)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Введен неправильный код безопасности!\n'
                                          'Письмо не было отослано.\nГуляй отсюда петушок')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ты должен передать /vodichka и 3 числа:\n'
                                      '1. Проверочный код\n'
                                      '2. Холодная вода\n'
                                      '3. Горячая вода\n')

def settings(update, context):
    try:
        if not os.path.exists(file):
            with open(file, 'w'): pass
        username = update['message']['chat']['username']
        context.bot.send_message(chat_id=update.effective_chat.id, text="Привет @%s !" % username)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Введите почтовый ящик, "
                                                                        "с которого будет письмо.")

        # updater.dispatcher.add_handler(MessageHandler(Filters.text,regular_choice))
    except Exception as exception:
        context.bot.send_message(chat_id=update.effective_chat.id,
                         text="Error: %s!\n\n" % exception)

def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

def understood(update, context):
    rnd = random.choice(["Да, понимаю тебя!", "Не, ну ты точно считаешь так?", "Лол", "Вот и моя мама так говорит"])
    context.bot.send_message(chat_id=update.effective_chat.id, text=rnd)

def done(update, context):
    try:
        user_data = context.user_data
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_text("Okay, boomer")

        updater.dispatcher.remove_handler(MessageHandler(Filters.text,regular_choice))
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

    # updater.dispatcher.add_handler(CommandHandler('start', start))
    # updater.dispatcher.add_handler(CommandHandler('vasilich', vasilich))
    # updater.dispatcher.add_handler(CommandHandler('vodichka', vodichka))
    # updater.dispatcher.add_handler(CommandHandler('settings', settings))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('vasilich', vasilich),
                      CommandHandler('vodichka', vodichka),
                      CommandHandler('settings', settings),],

        states={
            # CHOOSING: [CommandHandler('vasilich', vasilich),
            #            CommandHandler('vodichka', vodichka),
            #            CommandHandler('settings', settings),
            #            ],
             # CHOOSING: [MessageHandler(Filters.regex('^(Age|Favourite colour|Number of siblings)$'),
             CHOOSING: [MessageHandler(Filters.regex('^(Email|Code|User|Password|To)'),
                                       regular_choice)
                        ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           understood)
                            ],

            # TYPING_REPLY: [MessageHandler(Filters.text,
            #                               received_information),
            #                ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()