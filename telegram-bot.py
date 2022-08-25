import telebot
import json
from telebot import types
import config
import os
import pathlib
import requests


BASE_DIR = pathlib.Path(__file__).parent.resolve()
GROUPS_FILE = os.path.join(BASE_DIR, "groups.json")

API_TOKEN = config.API_TOKEN
CHECK = requests.get(f"https://api.telegram.org/bot{config.API_TOKEN}/getMe")
print(CHECK)

bot = telebot.TeleBot(API_TOKEN)
BOT = bot.get_me()


def send_to_groups(chat_id):
    address = config.CLIENT.get(f"address-{chat_id}")
    photo = config.CLIENT.get(f"photo-{chat_id}")
    comment = config.CLIENT.get(f"comment-{chat_id}")
    if not (address or photo or comment):
        return
    config.CLIENT.delete(f"address-{chat_id}")
    config.CLIENT.delete(f"photo-{chat_id}")
    config.CLIENT.delete(f"photo-{chat_id}")
    address = json.loads(address)
    try:
        with open(GROUPS_FILE, "r") as file:
            for cid in json.loads(file.read())['groups']:
                bot.send_location(cid, address['latitude'], address['longitude'])
                bot.send_photo(cid, photo)
                bot.send_message(cid, comment)
        print("success")
    except Exception as e:
        bot.send_message(chat_id, "Қате, қайтадаң қайталап көріңіз", reply_markup=general_markup())


def general_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keys = ['Ақпарат', 'Жалоба']
    for key in keys:
        markup.add(types.KeyboardButton(key))
    return markup


def handle_photo(message):
    if not message.photo:
        bot.send_message(message.chat.id, "Суретті жіберіңіз")
        bot.register_next_step_handler(message, handle_photo)
    config.CLIENT.set(f"photo-{message.chat.id}", message.photo[-1].file_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Мекен-жайды жіберу", request_location=True), types.KeyboardButton("Тоқтату"))
    bot.send_message(message.chat.id, "Мекен-жайды жіберу үшін сәйкес батырманы басыңыз", reply_markup=markup)
    bot.register_next_step_handler(message, handle_address)


def handle_address(message):
    if message.text == "Тоқтату":
        bot.send_message(message.chat.id, "Батырманы басыңыз", reply_markup=general_markup())
    else:
        if not message.location:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Мекен-жайды жіберу", request_location=True), types.KeyboardButton("Тоқтату"))
            bot.send_message(message.chat.id, "Мекен-жайды жіберу үшін сәйкес батырманы басыңыз", reply_markup=markup)
            bot.register_next_step_handler(message, handle_address)
        location = json.dumps({
            'latitude': message.location.latitude,
            'longitude': message.location.longitude
        })
        config.CLIENT.set(f"address-{message.chat.id}", location)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Тоқтату"))
        bot.send_message(message.chat.id, "Комментария", reply_markup=markup)
        bot.register_next_step_handler(message, handle_comments)


def handle_comments(message):
    if message.text == "Тоқтату":
        bot.send_message(message.chat.id, "Батырманы басыңыз", reply_markup=general_markup())
    else:
        config.CLIENT.set(f"comment-{message.chat.id}", message.text)
        send_to_groups(message.chat.id)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бұл 'Тілге құрмет - елге құрмет' жобасы.", reply_markup=general_markup())


def validate_and_add(message):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == config.AUTH_PWD:
        with open(GROUPS_FILE, "a") as file:
            try:
                data = json.load(file)
            except Exception as e:
                data = {}
        with open(GROUPS_FILE, 'w') as file:
            groups = data['groups'] if data.get('groups') else []
            if message.chat.id not in groups:
                groups.append(message.chat.id)
            data['groups'] = groups
            json.dump(data, file)
        bot.send_message(message.chat.id, "Группа сәтті қосылды")
    else:
        bot.send_message(message.chat.id, "Құпия сөз қате")


@bot.message_handler(commands=['register'])
def register(message):
    admins = bot.get_chat_administrators(message.chat.id)
    permission = False
    for admin in admins:
        if admin.user.id == BOT.id:
            if admin.can_delete_messages:
                permission = True
    if permission is False:
        bot.send_message(message.chat.id, "Админ рұқсатың ботқа беріңіз")
    else:
        bot.send_message(message.chat.id, "Құпия сөз")
        bot.register_next_step_handler(message, validate_and_add)


@bot.message_handler(content_types="text")
def handle_text(message):
    if message.text == "Ақпарат":
        with open(os.path.join(BASE_DIR,"info.txt"), "r") as file:
            text = file.read()
        bot.send_message(message.chat.id, text)
    elif message.text == "Жалоба":
        bot.send_message(message.chat.id, "Сурет жберіңіз")
        bot.register_next_step_handler(message, handle_photo)


bot.infinity_polling()