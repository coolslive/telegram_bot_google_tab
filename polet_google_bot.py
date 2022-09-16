from datetime import date
from telebot import types
import telebot
import gspread


token = 'УКАЗЫВАЕМ СВОЙ ТОКЕН'
googlesheet_id = 'АЙДИ ГУГУЛ ТАБЛИЦЫ'
bot = telebot.TeleBot(token)
gc = gspread.service_account(filename='charged-sled-359915-6642a1593084.json')


@bot.message_handler(commands=['button'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Лист1', callback_data='list_1')
    item2 = types.InlineKeyboardButton('Лист2', callback_data='list_2')
    markup.add(item, item2)

    bot.send_message(message.chat.id, 'Привет, выберите вкладку.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    bot.answer_callback_query(callback_query_id=call.id)
    if call.message:
        if call.data == 'list_1':
            bot.send_message(call.message.chat.id, 'Выбран ЛИСТ1. Внесите данные через ДЕФИЗ в формате: [КАТЕГОРИЯ-СУММА-КОММЕНТАРИЙ]')
            @bot.message_handler(content_types=["text"])
            def repeat_all_messages(message):
                try:
                    today = date.today().strftime("%d.%m.%Y")

                    category, price, comments = message.text.split("-", 2)
                    text_message = f'На {today} в таблицу внесена запись: категория - {category}, сумма - {price}, комментарий - {comments}'
                    bot.send_message(message.chat.id, text_message)

                    sh = gc.open_by_key(googlesheet_id)
                    sh.get_worksheet(0).append_row([today, category, price, comments])
                except:
                    bot.send_message(message.chat.id, 'ОШИБКА! Неправильный формат данных!')

                bot.send_message(message.chat.id, 'Внесите данные через ДЕФИЗ в формате: [КАТЕГОРИЯ-СУММА-КОММЕНТАРИЙ] или вернитесь к выбору вкладки - /button')

        elif call.data == 'list_2':
            bot.send_message(call.message.chat.id, 'Выбран ЛИСТ2. Внесите данные через ДЕФИЗ в формате: [КАТЕГОРИЯ-СУММА-КОММЕНТАРИЙ]')
            @bot.message_handler(content_types=["text"])
            def repeat_all_messages(message):
                try:
                    today = date.today().strftime("%d.%m.%Y")

                    category, price, comments = message.text.split("-", 2)
                    text_message = f'На {today} в таблицу внесена запись: категория - {category}, сумма - {price}, комментарий - {comments}'
                    bot.send_message(message.chat.id, text_message)

                    sh = gc.open_by_key(googlesheet_id)
                    sh.get_worksheet(1).append_row([today, category, price, comments])
                except:
                    bot.send_message(message.chat.id, 'ОШИБКА! Неправильный формат данных!')

                bot.send_message(message.chat.id, 'Выбран ЛИСТ2. Внесите данные через ДЕФИЗ в формате: [КАТЕГОРИЯ-СУММА-КОММЕНТАРИЙ] или вернитесь к выбору вкладки - /button')

if __name__ == '__main__':
     bot.polling(none_stop=True)