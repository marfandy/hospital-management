import datetime
from datetimerange import DateTimeRange


def format_check(date, fmt):
    try:
        datetime.datetime.strptime(date, fmt)
        return True
    except:
        return False


def schedule_check(daterime_pick: str, start_date: datetime.time, end_date: datetime.time) -> bool:
    date_pick = datetime.datetime.strptime(
        daterime_pick.split()[0], '%Y-%m-%d')
    start_date = datetime.datetime.combine(date_pick, start_date)
    end_date = datetime.datetime.combine(date_pick, end_date)

    time_range = DateTimeRange(start_date, end_date)

    if daterime_pick in time_range:
        return True
    return False
