import telebot, sqlite3, datetime, pytz
from telebot import types

bot = telebot.TeleBot('5308126595:AAG08b3BIlDCtqBH4Iq8lNFVpLHA7rbjn5o')
chat_id_user = '-891875260'  # id чата  с пользователем
chat_id_admins = '-1001688181513'  # id чата с админами
chat_id_tickets = '-856880830'  # id чата с поддержкой
conn = sqlite3.connect('db/botDB.db', check_same_thread=False)
cursor = conn.cursor()
dt = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
date = datetime.date.today().strftime("%d/%m/%Y")
time = dt.time().strftime('%H:%M:%S')
ticket_counter = 0
pc_numbers = ''


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, message_id: int, message_text: str):
    try:
        cursor.execute(
            'INSERT INTO botlog (user_id, user_name, user_surname, username,message_id,message_text) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, user_name, user_surname, username, message_id, message_text))
        conn.commit()
    except Exception as ex_pict:
        print(str(ex_pict) + ' (DB EXCEPTION)')


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'])
def get_text_messages(message):
    try:
        if message.chat.id == int(chat_id_user):
            if message.text == '/ticket@cyberxproblems_bot' or message.text == '/ticket':
                keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
                key_abort = types.InlineKeyboardButton(text='Отмена', callback_data='abort')
                keyboard.add(key_abort)
                bot.send_message(chat_id=chat_id_user,
                                 text='Введите номер ПК', reply_markup=keyboard)
                bot.register_next_step_handler(message, pc_number)
                bot.send_message(chat_id=chat_id_user,
                                 text='Введите номер ПК и описание проблемы', reply_markup=keyboard)
                bot.register_next_step_handler(message, message_user, None)
            elif message.text == '/help' or message.text == '/help@cyberxproblems_bot':
                bot.send_message(chat_id=chat_id_user,
                                 text='/ticket - Отправка тикета\n/ticketstop - Отмена тикета\n/help - Вызов справки по боту')
            elif '/' in str(message.text):
                bot.send_message(chat_id=chat_id_user,
                                 text='Неверная команда,введите /help для отображения списка команд')
        else:
            message_user(message, pc_numbers)
    except Exception as ex_get:
        print(str(ex_get) + ' (GET EXCEPTION)')


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'])
def message_user(message,number):
    global ticket_counter, pc_numbers
    try:
        if message.text == '/ticketstop@cyberxproblems_bot' or message.text == '/ticketstop':
            return
        if message.chat.id == int(chat_id_user):
            ticket_counter += 1
            bot.send_message(chat_id=chat_id_tickets, text='-------------------------------------\n' + str(
                str(date) + '    ' + str(time) + '\n' + 'Номер тикета: ' + '#' + str(
                    ticket_counter) + '\n\n'
                                      f'@{message.from_user.username}\n') + 'Номер ПК: ' + str(
                pc_number(message)) + '\n' + message.text + '\n' + '-------------------------------------\n')  # пересылка ответа пользователя в чат с поддержкой
        elif message.chat.id == int(chat_id_tickets) and message.reply_to_message:
            m = message.reply_to_message.text.split('\n')
            del m[0:5]
            m.pop()
            a = '\n'.join(m)
            replay: str = message.reply_to_message.text.split('\n')[
                              4] + '\n' + '-------------------------------------' + '\n' + 'Вопрос пользователя:' + '\n' + a + '\n' + 'Ответ админа:' + '\n' + message.text + '\n' + '-------------------------------------'
            bot.send_message(chat_id=int(chat_id_user), text=replay)  # пересылка ответа поддержки в чат с пользователем

        # ==========DEBUG MESSAGES======================
        # print(message.reply_to_message)
        print(log_msg(message))
        # print('ARRAY LENGHT: ' + str(len(message.reply_to_message.text.split('\n')))+'\n')
    except Exception as ex_send:
        print(str(ex_send) + ' (SENDER EXCEPTION)\n')


def pc_number(message):
    global pc_numbers
    pc_numbers = str(message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "abort":
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)


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
    print(str(ex_poll) + ' (UPDATER EXCEPTION)\n')
