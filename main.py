import telebot

from telebot import types
from telebot import util

from parse import Parser

parser_kuhnya = Parser('https://povar.ru/list/')

bot = telebot.TeleBot('YOUR_ACCESS_TOKEN')
print('Server started')


@bot.message_handler(commands=['start'])
def welcome(message):
    img = open('intro.jpg', 'rb')
    bot.send_sticker(message.chat.id, img)
    img.close()
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🍛Горячие блюда")
    item2 = types.KeyboardButton("🥙Салаты")
    item3 = types.KeyboardButton("🥪Закуски")
    item4 = types.KeyboardButton("🍲Супы")
    item5 = types.KeyboardButton("🥐Выпечка")
    item6 = types.KeyboardButton("🍨Десерты")
    item7 = types.KeyboardButton("☕Напитки")
    item8 = types.KeyboardButton("🍾Соусы")
    item9 = types.KeyboardButton("🥫Заготовки")
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь вам с готовкой. Что вас интересует?".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def chats(message):
    if message.chat.type == 'private':
        if message.text == '🍛Горячие блюда':
            text = parser_kuhnya.get_available_recipes("Горячие блюда")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        elif message.text == '🥙Салаты':
            text = parser_kuhnya.get_available_recipes("Салаты")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        elif message.text == '🥪Закуски':
            text = parser_kuhnya.get_available_recipes("Закуски")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        if message.text == '🍲Супы':
            text = parser_kuhnya.get_available_recipes("Супы")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        elif message.text == '🥐Выпечка':
            text = parser_kuhnya.get_available_recipes("Выпечка")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        elif message.text == '🍨Десерты':
            text = parser_kuhnya.get_available_recipes("Десерты")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        elif message.text == '☕Напитки':
            text = parser_kuhnya.get_available_recipes("Напитки")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        elif message.text == '🍾Соусы':
            text = parser_kuhnya.get_available_recipes("Соусы")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)
        elif message.text == '🥫Заготовки':
            text = parser_kuhnya.get_available_recipes("Заготовки")
            bot.send_message(message.chat.id, "Выберите блюдо из предложенных ниже:")
            bot.send_message(message.chat.id, text)

        elif message.text != "/start":
            text = message.text[0].upper() + message.text[1::]
            result = parser_kuhnya.get_recipe_info(text)
            if result is not None:
                bot.send_photo(message.chat.id, result["imgSrc"], caption=result["dishName"])
                # bot.send_message(message.chat.id, result["dishName"])
                bot.send_message(message.chat.id, result["ingredients"])
                if len(result["steps"]) > 0:
                    bot.send_message(message.chat.id, result["steps"])

                with open("anime.jpg", "rb") as animephoto:
                    bot.send_photo(message.chat.id, animephoto,
                                   caption="Полное описание рецепта: {}".format(result["url"]))


# RUN
bot.polling(none_stop=True)
