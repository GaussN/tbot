from datetime import datetime, time, timedelta

from config import BELLS


'''
Ищет время до начала след пары и до конца текущей 
возвращает: кортеж(время до начала пары, время до конца пары)
'''
def time_to_bell():
    now = datetime.now()
    week_day = datetime.weekday(now)
    
    time_until_call_from_class = 0 # время до звонока с урока 
    time_before_class_call = 0 # время до звонка на урок

    for bell_time in BELLS[week_day]:
        lesson_start = datetime.strptime(bell_time[0], '%H.%M')
        if now.time() < lesson_start.time():
            print("след пара начнется\t", lesson_start)
            time_before_class_call = (lesson_start - timedelta(hours=now.hour, minutes=now.minute)).time()
            break
    
    for bell_time in BELLS[week_day]:
        lesson_end = datetime.strptime(bell_time[1], '%H.%M')
        if now.time() < lesson_end.time():
            print("пара закончися в \t", lesson_end)
            time_until_call_from_class= (lesson_end - timedelta(hours=now.hour, minutes=now.minute)).time() 
            break

    return (time_before_class_call, time_until_call_from_class)