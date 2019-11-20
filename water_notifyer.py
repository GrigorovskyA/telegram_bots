import telegram, smtplib

from datetime import datetime
from telegram.ext import Updater, CommandHandler
from variables import *

bot = telegram.Bot(token)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, Mr. and Mrs. Grigorovsky.")

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

if proxy_kwargs:
    updater = Updater(token, use_context=True, request_kwargs=proxy_kwargs)
else:
    updater = Updater(token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('vasilich', vasilich))
updater.dispatcher.add_handler(CommandHandler('vodichka', vodichka))

updater.start_polling()