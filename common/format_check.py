import datetime


def format_check(date, fmt):
    try:
        datetime.datetime.strptime(date, fmt)
        return True
    except:
        return False
