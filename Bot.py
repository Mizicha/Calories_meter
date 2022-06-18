from email import message
import telebot
from f import *
from telebot import types

bot = telebot.TeleBot('5375003782:AAEEMc-ZFaNZhVOsTJz7ci2zpgOydGJCIVM');


@bot.message_handler(commands=['start'])
def buttons(message):
    global user_id
    user_id = message.from_user.id
    if (message.from_user.username == ""):
        user_nick = "default"
    else:
        user_nick = message.from_user.username
    if(user_select(user_id) != user_id):
        new_user(user_id, user_nick)
    markup = types.InlineKeyboardMarkup(row_width = 1)
    item = types.InlineKeyboardButton(text='Начать', callback_data='back')
    markup.add(item)
    bot.send_message(message.chat.id, text = "Начало", reply_markup = markup) 

def begin(call):
    markup = types.InlineKeyboardMarkup(row_width = 3)
    item = types.InlineKeyboardButton(text='Статус', callback_data='status') 
    item_2 = types.InlineKeyboardButton(text='Продукты', callback_data='products') 
    item_3 = types.InlineKeyboardButton(text='Вес', callback_data='weight') 
    markup.add(item, item_2, item_3)
    bot.send_message(call.message.chat.id, text = "Меню", reply_markup = markup)

def get_weight(message):
    bot.send_message(message.chat.id, text = "Введите свой вес")
    bot.register_next_step_handler(message, weight_add)
    
def del_weight(message):
    bot.send_message(message.chat.id, text = "Введите ID удаляемой записи")
    bot.register_next_step_handler(message, weight_delete)

def get_products(message):
    bot.send_message(message.chat.id, text = "Добавьте новый продукт в формате: Название, Белки, Жиры, Углеводы")
    bot.register_next_step_handler(message, products_add)
    
def del_products(message):
    bot.send_message(message.chat.id, text = "Введите ID удаляемой записи")
    bot.register_next_step_handler(message, products_delete)
    
def get_today(message):
    bot.send_message(message.chat.id, text = "Добавьте запись в формате: Название, вес")
    bot.register_next_step_handler(message, today_add)
    
def del_today(message):
    bot.send_message(message.chat.id, text = "Введите ID удаляемой записи")
    bot.register_next_step_handler(message, today_delete)
    
@bot.callback_query_handler(func=lambda call: True)    
def callback(call):
    if call.data == "status": 
        status(call)
    elif call.data == "products":
        products(call)
    elif call.data == "products_add":
        get_products(call.message)
    elif call.data == "products_delete":
        del_products(call.message)
    elif call.data == "weight":
        weight(call)
    elif call.data == "weight_add":
        get_weight(call.message)
    elif call.data == "weight_delete":
        del_weight(call.message)
    elif call.data == "today_add":
        get_today(call.message)
    elif call.data == "today_delete":
        del_today(call.message)
    elif call.data == "back":
        begin(call)  
        
def status(call):
    markup = types.InlineKeyboardMarkup(row_width = 3)
    item = types.InlineKeyboardButton(text='Добавить', callback_data='today_add')
    item_2 = types.InlineKeyboardButton(text='Удалить', callback_data='today_delete')
    item_3 = types.InlineKeyboardButton(text='Назад', callback_data='back') 
    markup.add(item, item_2, item_3)

    bot.send_message(call.message.chat.id, select_status(user_id), reply_markup = markup)    
    
def today_add(message):
    product_info = message.text
    product_split = product_info.split(", ")
    
    bot.send_message(message.chat.id, text = dbtoday_add(product_split[0], product_split[1], user_id))
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    item = types.InlineKeyboardButton(text='Ещё', callback_data='today_add')
    item_2 = types.InlineKeyboardButton(text='Назад', callback_data='status')
    markup.add(item, item_2)
    bot.send_message(message.chat.id, text = "Статус - Добавить", reply_markup = markup)
    
def today_delete(message):
    tid = message.text
    dbtoday_delete(tid, user_id)
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    item = types.InlineKeyboardButton(text='Ещё', callback_data='today_delete')
    item_2 = types.InlineKeyboardButton(text='Назад', callback_data='status')
    markup.add(item, item_2)
    bot.send_message(message.chat.id, text = "Статус - Удалить", reply_markup = markup)

def products(call):
    s = select_products(user_id)
    if (s == ""):
        bot.send_message(call.message.chat.id, text = "Записей нет")    
    else: 
        bot.send_message(call.message.chat.id, text = s)

    markup = types.InlineKeyboardMarkup(row_width = 3)
    item = types.InlineKeyboardButton(text='Добавить продукт', callback_data='products_add') 
    item_2 = types.InlineKeyboardButton(text='Удалить продукт', callback_data='products_delete') 
    item_3 = types.InlineKeyboardButton(text='Назад', callback_data='back')
    markup.add(item, item_2, item_3)
    
    bot.send_message(call.message.chat.id, text = "Продукты", reply_markup = markup)

def products_add(message):
    
    product_info = message.text
    product_split = product_info.split(", ")
    print(product_split[0], product_split[1], product_split[2], product_split[3])
    add_products(product_split[0], product_split[1], product_split[2], product_split[3], user_id)
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    item = types.InlineKeyboardButton(text='Ещё', callback_data='products_add')
    item_2 = types.InlineKeyboardButton(text='Назад', callback_data='products')
    markup.add(item, item_2)
    bot.send_message(message.chat.id, text = "Продукты - Добавить", reply_markup = markup)

def products_delete(message):
    tid = message.text
    dbproducts_delete(tid, user_id)
    markup = types.InlineKeyboardMarkup(row_width = 2)
    item = types.InlineKeyboardButton(text='Ещё', callback_data='products_delete')
    item_2 = types.InlineKeyboardButton(text='Назад', callback_data='products')
    markup.add(item, item_2)
    bot.send_message(message.chat.id, text = "Продукты - Удалить", reply_markup = markup)
    
def weight(call):
    weight_select = select_weight(user_id)
    bot.send_message(call.message.chat.id, text = weight_select)
    
    markup = types.InlineKeyboardMarkup(row_width = 3)
    item = types.InlineKeyboardButton(text='Добавить запись', callback_data = 'weight_add') 
    item_2 = types.InlineKeyboardButton(text='Удалить запись', callback_data = 'weight_delete') 
    item_3 = types.InlineKeyboardButton(text='Назад', callback_data='back')
    markup.add(item, item_2, item_3)
    
    bot.send_message(call.message.chat.id, text = "Вес", reply_markup = markup)
    
def weight_add(message):
    uweight = message.text
    weight_insert(uweight, user_id)
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    item = types.InlineKeyboardButton(text='Ещё', callback_data='weight_add')
    item_2 = types.InlineKeyboardButton(text='Назад', callback_data='weight')
    markup.add(item, item_2)
    bot.send_message(message.chat.id, text = "Вес - Добавить", reply_markup = markup)

def weight_delete(message):
    tid = message.text
    dbweight_delete(tid, user_id)
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    item = types.InlineKeyboardButton(text='Ещё', callback_data='weight_delete')
    item_2 = types.InlineKeyboardButton(text='Назад', callback_data='weight')
    markup.add(item, item_2)
    bot.send_message(message.chat.id, text = "Вес - Удалить", reply_markup = markup)
    
bot.polling(none_stop=True, interval=0)