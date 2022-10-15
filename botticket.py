from email import message

import telebot;
import update as update
from telebot import types
import logging

bot = telebot.TeleBot('5308126595:AAG08b3BIlDCtqBH4Iq8lNFVpLHA7rbjn5o')
chat_id_user = '-1001784446207'  # id чата  с пользователем
chat_id_self = '445283271'  # id чата с ботом
chat_id_tickets = '-814258509 '  # id чата с поддержкой


# @bot.message_handler(content_types=['text', 'document', 'audio', 'photo'], commands=['start', 'ticket'])
# def get_text_messages(message):
#     if message.text == "/ticket":
#         bot.send_message(chat_id=chat_id_user,
#                          text='Введите номер ПК и описание проблемы')  # запрос сообщения в чате с пользователем
@bot.message_handler(func=lambda message2: True)
def message_receive(message_user):
    if chat_id_user:
        bot.send_message(chat_id=chat_id_user,
                        text=message_user.text)  # пересылка ответа пользователя в чат с поддержкой
    log_msg(message_user)
    print('USER')
    message_send(message_user)
@bot.message_handler(func=lambda message1: True)
def message_send(message_ticket):
    if chat_id_tickets:
        bot.send_message(chat_id=chat_id_tickets, text=message_ticket.text)  # пересылка ответа поддержки в чат с пользователем
    log_msg(message_ticket)
    print('TICKET')





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
