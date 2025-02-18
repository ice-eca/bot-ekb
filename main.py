import telebot
from telebot import types
import re

TOKEN = '6546041003:AAGFsIk0Mgbc2aD5raqko-Xrmgelnk02ro8'

bot = telebot.TeleBot(TOKEN)

phone_number_regex = re.compile(r'^(\+7|8)\d{10}$')
age_regex = re.compile(r'^\d.*')
district_regex = re.compile(r'^\D.*')
data = {}
request_chat_id = '-1002088344075'

@bot.message_handler(commands=['start'])

def enter_district(message):
    clear_data(message)
    data[message.chat.id] = {'stage':0}
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='Центр', callback_data='Центр')
    itembtn2 = types.InlineKeyboardButton(text='ВИЗ', callback_data='ВИЗ')
    itembtn3 = types.InlineKeyboardButton(text='Ботаника', callback_data='Ботаника')
    itembtn4 = types.InlineKeyboardButton(text='Академ', callback_data='Академ')
    itembtn5 = types.InlineKeyboardButton(text='Пышма', callback_data='Пышма')
    itembtn6 = types.InlineKeyboardButton(text='Клевер Парк', callback_data='Клевер Парк')
    itembtn7 = types.InlineKeyboardButton(text='Автовокзал', callback_data='Автовокзал')
    itembtn8 = types.InlineKeyboardButton(text='ЖБИ', callback_data='ЖБИ')
    itembtn9 = types.InlineKeyboardButton(text='Уралмаш', callback_data='Уралмаш')
    
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)
    bot.send_photo(message.chat.id, open('kiber1.png', 'rb'))
    bot.send_message(message.chat.id, 'Школа программирования для детей KIBERone Екатеринбург приветствует вас!\U0001F60A\n \nНа этой неделе мы проводим бесплатный мастер-класс по программированию для детей 6-14 лет.\n \n\U00002705Ваш ребенок создаст свой первый мультфильм и запрограммирует своего героя в игре Майнкрафт.\n \n\U00002705Расскажем, как избавить ребенка от игромании и научить компьютерной грамотности, чтобы подготовить к успешному будущему.\n \n\U00002705Длительность занятия 60 минут. Все необходимое предоставим. Ничего брать с собой не нужно.\n \nВыберите удобный для Вас район\U0001F447' , reply_markup=markup)
    
def enter_age(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='6-8 лет', callback_data='6-8')
    itembtn2 = types.InlineKeyboardButton(text='9-11 лет', callback_data='9-11')
    itembtn3 = types.InlineKeyboardButton(text='12-14 лет', callback_data='12-14') 
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, 'Пожалуйста, укажите возраст вашего ребенка\U0001F447',reply_markup=markup)


def enter_phone_number(message):
    bot.send_message(message.chat.id, 'Спасибо! Остался последний шаг\U0001F60A\n \nПожалуйста, введите номер телефона, по которому мы можем с Вами связаться\U0001F4F1')
    
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.startswith('/start'):
        return
    if message.text.startswith('/getID'):
        bot.send_message(message.chat.id, message.chat.id)
        return
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Неверная команда')
        return
    if phone_number_regex.match(message.text) and data[message.chat.id]['stage'] == 2:
        data[message.chat.id]['phone_number'] = message.text
        data[message.chat.id]['stage'] = 3
        check_and_send(message)
        return
    else:
        bot.send_message(message.chat.id, 'Повторите попытку')
        return

def check_and_send(message):
    if district_regex.match(data[message.chat.id]['district']) and age_regex.match(data[message.chat.id]['age']):
        bot.send_message(message.chat.id, 'Спасибо! Скоро с Вами свяжется наш менеджер и отправит вам расписание пробных занятий на ближайшую неделю и согласует точное время.\n \nДо встречи на уроке!\U0001F60A')
        bot.send_message(request_chat_id, '\U00002757\U00002757\U00002757 Новый лид\U00002757\U00002757\U00002757'+'\nРайон: ' + data[message.chat.id]['district']+'\nВозраст: '+data[message.chat.id]['age']+'\nТел: '+data[message.chat.id]['phone_number'])
        clear_data(message)
    else:
        bot.send_message(message.chat.id, 'Неправильно сформированы ответы на вопросы, поробуйте еще раз')
        enter_district(message)
    
def clear_data(message):
    if message.chat.id in data:
        del data[message.chat.id]
  
@bot.callback_query_handler(func=lambda call: True)
def answering(call):
    if call.message.chat.id in data:
        if data[call.message.chat.id]['stage'] == 0:
            data[call.message.chat.id]['district'] = call.data
            data[call.message.chat.id]['stage'] = 1
            enter_age(call.message)
        elif data[call.message.chat.id]['stage'] == 1:
            data[call.message.chat.id]['age'] = call.data
            data[call.message.chat.id]['stage'] = 2
            enter_phone_number(call.message)
bot.infinity_polling()
