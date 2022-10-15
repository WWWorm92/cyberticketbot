from email import message

import telebot;
from telebot import types
import logging

bot = telebot.TeleBot('5308126595:AAG08b3BIlDCtqBH4Iq8lNFVpLHA7rbjn5o')


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'])
def get_text_messages(message):
    bool = 'no'
    if message.text == "/ticket":
        bot.send_message(message.from_user.id)  # КНОПКИ
    log_msg(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "close":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # код сохранения данных, или их обработки
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        #bot.delete_message(call.message.chat.id, call.message.message_id)


def log_msg(msg):
    mcfn = str(msg.chat.first_name)
    mcln = str(msg.chat.last_name)
    mcid = str(msg.chat.id)
    muid = str(msg.from_user.id)
    print('=================================================================================')
    if mcln != 'None':
        print(f"Message from {mcfn} {mcln}  ,Chat iD: {mcid} ,User ID: {muid}")
    else:
        print(f"Message from {mcfn} ,Chat iD: {mcid} ,User ID: {muid}")
    print('Text:', str(msg.text))
    print('=================================================================================')


try:
    bot.polling(interval=1, timeout=2)
    # bot.infinity_polling()
except Exception as ex1:
    print(ex1)