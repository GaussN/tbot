from datetime import datetime, timedelta

from loguru import logger

from loader import schedule_parser
from config import BELLS


'''
Ищет время до начала след пары и до конца текущей 
возвращает: 
            кортеж(время до начала пары, время до конца пары)       
или
            кортеж(время начала пары, None)

'''
@logger.catch
def time_to_bell():
    now = datetime.now()
    week_day = datetime.weekday(now)

    current_day_lessons = schedule_parser.get_schedule(week_day % 7)
    next_day_lessons = schedule_parser.get_schedule((week_day + 1) % 7)
    
    current_day_lesson_last: int = 0
    next_day_lesson_first: int = 0

    # нахождение первой пары 
    for lesson in next_day_lessons:
        if lesson != []:
            break
        next_day_lesson_first += 1

    # нахождение последней пары 
    for lesson in reversed(current_day_lessons):
        if lesson != []:
            break
        current_day_lesson_last += 1

    # проверка на окончиние пар
    current_day_lesson_last = len(current_day_lessons) - current_day_lesson_last - 1

    lesson_last_end_time = datetime.strptime(BELLS[week_day % 7][current_day_lesson_last][1], '%H.%M')
    if now.time() > lesson_last_end_time.time():
        '''
        если сегодня пары закончиличь, то возвращает
        время начала первой пары на след. день
        '''
        return (datetime.strptime(BELLS[(week_day + 1) % 7][next_day_lesson_first][0], '%H.%M'), None) 

    from_class = 0 # время до звонока с урока 
    to_class = 0 # время до звонка на урок

    for bell_time in BELLS[week_day]:
        lesson_start = datetime.strptime(bell_time[0], '%H.%M')
        print(bell_time, "\tdebug")
        if now.time() < lesson_start.time():
            to_class = (lesson_start - timedelta(hours=now.hour, minutes=now.minute)).time()
            break
    
    for bell_time in BELLS[week_day]:
        lesson_end = datetime.strptime(bell_time[1], '%H.%M')
        print(bell_time, "\tdebug")
        if now.time() < lesson_end.time():
            from_class = (lesson_end - timedelta(hours=now.hour, minutes=now.minute)).time() 
            break

    return (to_class, from_class)