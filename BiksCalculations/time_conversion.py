import datetime

def translate_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') # 2012-10-02 09:00:00

def calc_deltatime(t1, t2):
    diff = t2-t1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    return hours