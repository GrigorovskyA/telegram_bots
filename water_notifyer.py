import telegram, smtplib

from datetime import datetime
from telegram.ext import Updater, CommandHandler

token = '794614573:AAHSWRgPRwHYGwI6L4kYo6S7g3rOdfbuKNw'
our_code = '3366572'
gmail_user = 'grigorovsky.alexey@gmail.com'
gmail_app_password = 'PASS_SHOULD_BE_THERE'
bot = telegram.Bot(token)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, Mr. and Mrs. Grigorovsky.")

def vasilich(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Время сдавать показатели воды?\n'
                                                                    'Пришли показатели через /vodichka значение холодной '
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
                sent_to = ['elminster@mail.ru','katehollywood@mail.ru']
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Письмо было отослано на ' +
                                              ', '.join(sent_to) + ' ящики от ' + datetime.now().strftime("%m/%d/%Y"))

                sent_from = gmail_user
                sent_subject = "Показания воды за" + datetime.now().strftime("%m/%d/%Y")
                sent_body = ("Привет, Пишет тебе бот\n"
                             "Показания холодной воды: %s\n"
                             "Показания холодной воды: %s\n" % (cold_water, hot_water)
                             )

                email_text = """\
                From: %s
                To: %s
                Subject: %s
                
                %s
                """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_app_password)
                server.sendmail(sent_from, sent_to, email_text)
                server.close()
            except Exception as exception:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Error: %s!\n\n" % exception)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Введен неправильный код безопасности!\nПисьмо не было отослано.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ты должен передать 3 числа:\n'
                                      '1. Проверочный код\n'
                                      '2. Холодная вода\n'
                                      '3. Горячая вода\n')

updater = Updater(token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('vasilich', vasilich))
updater.dispatcher.add_handler(CommandHandler('vodichka', vodichka))

updater.start_polling()