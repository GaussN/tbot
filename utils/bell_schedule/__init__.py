'''
Отче наш, Иже еси на небесе́х!
Да святится имя Твое, да прии́дет Царствие Твое,
Да будет воля Твоя, яко на небеси́ и на земли́.
Хлеб наш насущный да́ждь нам дне́сь;
И оста́ви нам до́лги наша, якоже и мы оставляем должнико́м нашим;
И не введи нас во искушение, но изба́ви нас от лукаваго.
Яко Твое есть Царство и сила, и слава, Отца, и Сына, и Святаго Духа, ныне и присно, и во веки веков. Аминь.
'''
from datetime import datetime, timedelta

from loguru import logger

from loader import schedule_parser
from config import BELLS


@logger.catch
def get_last_lesson(lessons):
    lesson_last = len(lessons)
    for lesson in reversed(lessons):
        lesson_last -= 1
        if lesson != []:
            break

    return lesson_last


@logger.catch
def get_first_lesson(lessons):
    lesson_first = 0
    for lesson in lessons:
        if lesson != []:
            break
        lesson_first += 1

    return lesson_first


@logger.catch
def time_to_bell():
    now = datetime.now()
    week_day = min(5, datetime.weekday(now))
    # now = datetime.strptime('14.33', '%H.%M') # deb
    # week_day = 4 # deb 
    

    schedule = schedule_parser.get_schedule()

    last_lesson = get_last_lesson(schedule[week_day])

    end_time = datetime.strptime(BELLS[week_day][last_lesson][1], '%H.%M')

    # если пары закончились и сегодня суббота то никакого расписания до пн 
    if week_day >= 5 and now.time() > end_time.time():
        return (None, None)

    first_lesson = get_first_lesson(schedule[week_day+1])

    # если пары закончились или ещё не начались
    start_time = datetime.strptime(BELLS[week_day][first_lesson][0], '%H.%M')
    if now.time() > end_time.time() or now.time() < start_time.time():
        return (start_time, None)


    ### если пары ещё идут 
    from_class = 0 # время до звонока с урока 
    to_class = 0 # время до звонка на урок

    for bell_time in BELLS[week_day]:
        lesson_start = datetime.strptime(bell_time[0], '%H.%M')
        if now.time() < lesson_start.time():
            to_class = (lesson_start - timedelta(hours=now.hour, minutes=now.minute)).time()
            break
    
    for bell_time in BELLS[week_day]:
        lesson_end = datetime.strptime(bell_time[1], '%H.%M')
        if now.time() < lesson_end.time():
            from_class = (lesson_end - timedelta(hours=now.hour, minutes=now.minute)).time() 
            break
    ###

    return (to_class, from_class)