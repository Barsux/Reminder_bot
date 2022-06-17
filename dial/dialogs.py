from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from telebot import types
from fuzzywuzzy import fuzz
from dial.time_opt import date_interval2date, get_timedelta
from dial import REPEATS, get_default_markup
dials = []

def dials_exist():
    return len(dials) != 0

def find_dial(chat_id):
    for dial in dials:
        if dial.chat_id == chat_id:
            return dial
    else:
        return None

def reset_dial(chat_id):
    dial = find_dial(chat_id)
    if(dial):
        dials.remove(dial)

class Remind_Dialog():
    statement = "START_DIALOG"
    repeatonce = False
    repeat = None
    before = False
    def __init__(self, chat_id):
        dials.append(self)
        self.chat_id = chat_id

    def evaluate(self, data):
        reply = ""
        eval_again = False
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.statement == "START_DIALOG":
            reply = "О чём вам напомнить? Введите напоминание длиной менее 256 символов:"

            self.statement = "ASK_REMIND"
        elif self.statement == "ASK_REMIND":
            self.remind = data
            reply = f"Ваше напоминание: {self.remind}"
            eval_again = True

            self.statement = "ASK_DATE"
        elif self.statement == "ASK_DATE":
            reply = "Скажите когда вам напомнить", "Напишите дату (Например 12.02.22)", "Или напишите через сколько(Со словом через)"
            markup_reply.row("Завтра", "Через неделю", "Через две недели", "Через месяц")

            self.statement = "GET_DATE"
        elif self.statement == "GET_DATE":
            wrong_date = False
            if '.' in data and data.count('.') == 2:
                try:
                    self.date = datetime.strptime(data, "%d.%m.%y")
                except Exception:
                    wrong_date = True
                else:
                    if self.date < datetime.now():
                        wrong_date = True
            else:
                date, wrong_date = date_interval2date(data)
                if(not wrong_date):
                    self.date = date
            if wrong_date:
                reply = "Неправильная дата, введите заново"
            else:
                reply = ("Во сколько вам напомнить? По умолчанию 12:00", "Я могу напомнить вам во время кратное часу")
                markup_reply.row("По умолчанию", "6:00", "9:00", "12:00", "15:00", "18:00", "21:00")
                self.statement = "GET_TIME"
        elif self.statement == "GET_TIME":
            wrong_time = False
            if (len(data) == 4 or len(data) == 5) and data.count(':') == 1 and data.split(':')[1] == "00" and data.split(':')[0] != "00" :
                hours, _ = data.split(':')
                if hours.isdigit() and int(hours) < 24:
                    self.date += relativedelta(hours=int(hours))
                else:
                    wrong_time = True
            else:
                wrong_time = True
            if wrong_time:
                reply = "Неправильное время, введите заново"
            else:
                reply = f"Хорошо, я напомню вам в {self.date.strftime('%d.%m.%Y в %H:%M')}"
                eval_again = True

                self.statement = "ASK_REMIND_ONCE"

        elif self.statement == "ASK_REMIND_ONCE":
            reply = "Вам напомнить один раз или напоминать постоянно?"
            markup_reply.row("Один раз", "Постоянно")

            self.statement = "GET_REMIND_ONCE"
        elif self.statement == "GET_REMIND_ONCE":
            if data == "Один раз":
                self.repeatonce = True
                eval_again = True

                self.statement = "ASK_REMIND_BEFORE"
            elif data == "Постоянно":
                self.repeatonce = False
                eval_again = True

                self.statement = "ASK_REPEATS"
        elif self.statement == "ASK_REPEATS":
            reply = "Хорошо, буду повторять, с какой периодичностью?"
            markup_reply.row(*REPEATS)

            self.statement = "GET_REPEATS"
        elif self.statement == "GET_REPEATS":
            if data in REPEATS:
                self.repeat = REPEATS.index(data)
                eval_again = True

                self.statement = "ASK_REMIND_BEFORE"
            else:
                reply = "Неправильное значение повторов, введите ещё раз!"
        elif self.statement == "ASK_REMIND_BEFORE":
            reply = "Напоминать вам заранее?"
            markup_reply.row("Да", "Нет")

            self.statement = "GET_REMIND_BEFORE"
        elif self.statement == "GET_REMIND_BEFORE":
            if data == "Да":
                reply = "За сколько дней до даты вам напоминать? Максимум - неделя."
                markup_reply.row("За неделю", "за 3 дня", "за день")
                self.before = True
                self.statement = "GET_REMIND_BEFORE2"
            elif data == "Нет":
                self.before_date = self.date
                self.statement = "END_DIALOG"
                self.before = False
                eval_again = True
            else:
                reply = "Неправильный ответ, введите снова"
        elif self.statement == "GET_REMIND_BEFORE2":
            timedelt, wrong_date = get_timedelta(data)
            before_date = self.date - timedelt
            if wrong_date or before_date < datetime.now():
                reply = "Неправильная дата, введите снова"
            else:
                self.before_date = before_date

                eval_again = True
                self.statement = "END_DIALOG"
        elif self.statement == "END_DIALOG":
            reply = (
                "Отлично! Напоминание создано",
                f"Ваше напоминание: {self.remind}",
                f"Начну напоминать: {self.before_date.strftime('%d.%m.%Y  в %H:%M')}" if self.before else None,
                f"Буду повторять {REPEATS[self.repeat].lower()}" if not self.repeatonce else None,
                f"Конечная дата: {self.date.strftime('%d.%m.%Y  в %H:%M')}",
            )
            self.statement = "SUICIDE"
            return reply, get_default_markup(), True
        elif self.statement == "SUICIDE":
            dials.remove(self)
            return ("",), None, False
        markup_reply.add(types.KeyboardButton('Отмена'))
        if isinstance(reply, str):
            return (reply,) , markup_reply, eval_again
        else:
            return reply, markup_reply, eval_again
