import telebot
from telebot import types
token = "5318831729:AAG3RjJzkE0grk33iGqO7i1uXOzlCmbhlwY"
cli = telebot.TeleBot(token)

REPEATS = ("Каждую неделю", "Каждый месяц", "Каждый год")

NUMS_RAW = {
    'ноль': 0,
    'нуль': 0,
    'один': 1,
    'две': 2,
    'два': 2,
    'три': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'двадцать': 20,
    'тридцать': 30,
    'сорок': 40,
    'пятьдесят': 50,
    'шестьдесят': 60,
    'семьдесят': 70,
    'восемьдесят': 80,
    'девяносто': 90,
    'сто': 100,
    'двести': 200,
    'триста': 300,
    'четыреста': 400,
    'пятьсот': 500,
    'шестьсот': 600,
    'семьсот': 700,
    'восемьсот': 800,
    'девятьсот': 900,
    'тысяча': 10**3,
}

def get_default_markup():
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    set_remind = types.KeyboardButton('Добавить напоминание')
    get_reminds = types.KeyboardButton('Посмотреть свои напоминания')
    markup_reply.add(set_remind, get_reminds)
    return markup_reply

def replace_digits(string):
    string = string.lower()
    for word, value in list(NUMS_RAW.items())[::-1]:
        if word in string:
            string = string.replace(word, str(value))
    return string
