from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz
from dial import replace_digits

def date_interval2date(dateinterval):
    dateinterval = replace_digits(dateinterval)
    date = datetime.now().date()
    digit = 0
    for word in dateinterval.split():
        if word.isdigit():
            digit = int(word)
        elif word == "день" or word == "завтра":
            date += relativedelta(days=1)
        elif word == "неделю":
            date += relativedelta(weeks=1)
        elif word == "месяц":
            date += relativedelta(months=1)
        elif word == "год":
            date += relativedelta(years=1)
        elif fuzz.partial_ratio("дн", word) > 80:
            date += relativedelta(days=digit)
        elif fuzz.partial_ratio("недел", word) > 80:
            date += relativedelta(weeks=digit)
        elif fuzz.partial_ratio("месяц", word) > 80:
            date += relativedelta(months=digit)
        elif fuzz.partial_ratio("год", word) > 80:
            date += relativedelta(years=digit)
        elif fuzz.partial_ratio("лет", word) > 80:
            date += relativedelta(years=digit)
    return date, date == datetime.now().date()

def get_timedelta(dateinterval):
    dateinterval = replace_digits(dateinterval)
    date = relativedelta(days=0)
    digit = 0
    for word in dateinterval.split():
        if word.isdigit():
            digit = int(word)
        elif word == "день" or word == "завтра":
            date += relativedelta(days=1)
        elif word == "неделю":
            date += relativedelta(weeks=1)
        elif word == "месяц":
            date += relativedelta(months=1)
        elif word == "год":
            date += relativedelta(years=1)
        elif fuzz.partial_ratio("дн", word) > 80:
            date += relativedelta(days=digit)
        elif fuzz.partial_ratio("недел", word) > 80:
            date += relativedelta(weeks=digit)
        elif fuzz.partial_ratio("месяц", word) > 80:
            date += relativedelta(months=digit)
        elif fuzz.partial_ratio("год", word) > 80:
            date += relativedelta(years=digit)
        elif fuzz.partial_ratio("лет", word) > 80:
            date += relativedelta(years=digit)
    return date, date==relativedelta(days=0)

