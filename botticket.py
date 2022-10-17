import telebot, sqlite3, datetime
from telebot import types
import sys
bot = telebot.TeleBot('5308126595:AAG08b3BIlDCtqBH4Iq8lNFVpLHA7rbjn5o')
chat_id_user = '-1001784446207'  # id чата  с пользователем
chat_id_admins = '-1001688181513'  # id чата с админами
chat_id_tickets = '-857126611 '  # id чата с поддержкой
conn = sqlite3.connect('db/botDB.db', check_same_thread=False)
cursor = conn.cursor()
dt = datetime.datetime.now()
date = datetime.date.today().strftime("%Y/%M/%S")
time = dt.time().strftime('%H:%M:%S')
btn_close = 0
ticket_counter = 0


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, message_id: int, message_text: str):
    try:
        cursor.execute(
            'INSERT INTO botlog (user_id, user_name, user_surname, username,message_id,message_text) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, user_name, user_surname, username, message_id, message_text))
        conn.commit()
    except Exception as ex_pict:
        print(ex_pict)


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'])
def get_text_messages(message):
    global btn_close
    btn_close = 0
    if message.chat.id == int(chat_id_user):
        if message.text == '/ticket@cyberxproblems_bot' or message.text == '/ticket':
            keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
            key_abort = types.InlineKeyboardButton(text='Отмена', callback_data='abort')
            keyboard.add(key_abort)
            bot.send_message(chat_id=chat_id_user,
                             text='Введите номер ПК и описание проблемы', reply_markup=keyboard)
            print(str(btn_close) + 'old')
            bot.register_next_step_handler(message, message_user)

        elif message.text == '/help' or message.text == '/help@cyberxproblems_bot':
            bot.send_message(chat_id=chat_id_user,
                             text='/ticket - Отправка тикета\n/ticketstop - Отмена тикета\n/help - Вызов справки по боту')
        elif '/' in str(message.text):
            bot.send_message(chat_id=chat_id_user, text='Неверная команда,введите /help для отображения списка команд')
    else:
        message_user(message)


def message_user(message):
    global ticket_counter
    try:
        print(btn_close)
        if message.text == '/ticketstop@cyberxproblems_bot' or message.text == '/ticketstop' or btn_close == 1:
            return
        if message.chat.id == int(chat_id_user):
            ticket_counter += 1
            bot.send_message(chat_id=chat_id_tickets, text='-------------------------------------\n' + str(
                str(date) + '    ' + str(time) + '\n'+'Номер тикета: '+str(ticket_counter)+'\n'+'\n'
                                                 f'@{message.from_user.username}\n') + message.text +
                                                           '\n' + '-------------------------------------\n')  # пересылка ответа пользователя в чат с поддержкой
        elif message.chat.id == int(chat_id_tickets) and message.reply_to_message:
            replay: str = '-------------------------------------\n' + message.reply_to_message.text.split('\n')[
                2] + '\n' + 'Вопрос пользователя:' + '\n' + message.reply_to_message.text.split('\n')[
                              3] + '\n' + 'Ответ Админа:' + '\n' + message.text + '\n' + '-------------------------------------'
            bot.send_message(chat_id=int(chat_id_user), text=replay)  # пересылка ответа поддержки в чат с пользователем
        print(log_msg(message))
    except Exception as ex_send:
        print(ex_send)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global btn_close
    btn_close=0
    if call.data == "abort":
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        btn_close = 1
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        quit()


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
    # bot.polling(interval=1, timeout=2)
    bot.infinity_polling()
except Exception as ex_poll:
    print(ex_poll)
