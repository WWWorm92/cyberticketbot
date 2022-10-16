from email import message

import telebot
import sqlite3
import update as update
from telebot import types
import logging

bot = telebot.TeleBot('5308126595:AAG08b3BIlDCtqBH4Iq8lNFVpLHA7rbjn5o')
chat_id_user = '-1001784446207'  # id чата  с пользователем
chat_id_self = '445283271'  # id чата с ботом
chat_id_tickets = '-857126611 '  # id чата с поддержкой
conn = sqlite3.connect('db/botDB.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, message_id: int, message_text: str):
    cursor.execute(
        'INSERT INTO botlog (user_id, user_name, user_surname, username,message_id,message_text) VALUES (?, ?, ?, ?, ?, ?)',
        (user_id, user_name, user_surname, username, message_id, message_text))
    conn.commit()


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'], commands=['start', 'ticket'])
def get_text_messages(message):
    if message.text == "/ticket":
        bot.send_message(chat_id=chat_id_user,
                         text='Введите номер ПК и описание проблемы')  # запрос сообщения в чате с пользователем


@bot.message_handler()
def message_user(message):
    bot.send_message(chat_id=chat_id_tickets,
                     text=message.text)  # пересылка ответа пользователя в чат с поддержкой
    log_msg(message)
    print('USER')


@bot.message_handler()
def message_ticket(message):
    if message.chat.id == chat_id_tickets:
        bot.send_message(chat_id=chat_id_user, text=message.text)  # пересылка ответа поддержки в чат с пользователем
    log_msg(message)
    print('TICKET')


def log_msg(msg):
    mcfn = str(msg.chat.first_name)
    mcln = str(msg.chat.last_name)
    mcid = str(msg.chat.id)
    muid = str(msg.from_user.id)
    msgid = msg.message_id
    username = msg.from_user.username
    print('=================================================================================')
    if mcln != 'None':
        print(f"Message from {mcfn} {mcln}  ,Chat iD: {mcid} ,User ID: {muid} ,User Name:{username}")
        db_table_val(user_id=int(muid), user_name=mcfn, user_surname=mcln, username=username, message_id=msgid,
                     message_text=msg.text)
    else:
        print(f"Message from {mcfn} ,Chat iD: {mcid} ,User ID: {muid},User Name:{username}")
        db_table_val(user_id=int(muid), user_name=mcfn, user_surname=mcln, username=username, message_id=msgid,
                     message_text=msg.text)
    print('Text:', str(msg.text))
    print('=================================================================================')


try:
    bot.polling(interval=1, timeout=2)
    # bot.infinity_polling()
except Exception as ex1:
    print(ex1)
