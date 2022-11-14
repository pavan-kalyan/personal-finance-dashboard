import datetime


def format_time(dt, date=False):
    if not dt:
        return ""
    if dt == "":
        return dt
    if date:
        return dt.__format__('%Y-%m-%d')
    return dt.__format__('%Y-%m-%d %H:%M')
