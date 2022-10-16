import telebot
import sqlite3

bot = telebot.TeleBot('5308126595:AAG08b3BIlDCtqBH4Iq8lNFVpLHA7rbjn5o')
chat_id_user = '-1001784446207'  # id чата  с пользователем
chat_id_self = '445283271'  # id чата с ботом
chat_id_tickets = '-857126611 '  # id чата с поддержкой
conn = sqlite3.connect('db/botDB.db', check_same_thread=False)
cursor = conn.cursor()


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'], commands=['ticket', 'help', 'start'])
def get_text_messages(message):
    if message.text == '/ticket' or '/ticket@cyberxproblems_bot':
        bot.send_message(message.chat.id,
                         text='Введите номер ПК и описание проблемы')  # запрос сообщения в чате с пользователем
    elif message.text != '/ticket' or '/start' or '/help':
        bot.send_message(message.chat.id, text='Неверная команда,введите /help для отображения списка команд')


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'])
def message_user(message):
    #print(type(message.chat.id), type(chat_id_tickets), bool(message.reply_to_message))
    #print(message.chat.id == chat_id_tickets, bool(message.reply_to_message))
    if message.chat.id == int(chat_id_user):
        bot.send_message(chat_id=chat_id_tickets, text=str(
            f'@{message.from_user.username}\n') + message.text)  # пересылка ответа пользователя в чат с поддержкой
    elif message.chat.id == int(chat_id_tickets) and message.reply_to_message:
        #print('replay')
        #print(message.reply_to_message.text.split('\n')[0] + message.text)
        replay: str = message.reply_to_message.text.split('\n')[0] + '\n' + message.text
        bot.send_message(chat_id=int(chat_id_user), text=replay)  # пересылка ответа поддержки в чат с пользователем


try:
    bot.polling(interval=1, timeout=2)
    # bot.infinity_polling()
except Exception as ex1:
    print(ex1)
