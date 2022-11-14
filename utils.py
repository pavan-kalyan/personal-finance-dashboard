import datetime


def format_time(dt):
    if not dt:
        return ""
    if dt == "":
        return dt
    return dt.__format__('%Y-%m-%d %H:%M')
    # return datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M')