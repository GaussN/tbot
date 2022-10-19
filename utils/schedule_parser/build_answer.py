'''
Переводит список пар в читаемый вид
Возвращает: строку с уроками на день
'''
def build_day(lessons: list) -> str:
    res = ''

    buf = None
    num = 1
    counter = 0
    for lesson in lessons:
        if buf == None:
            buf = lesson
            continue
        elif buf == lesson:
            counter += 1
            continue
        else:
            if buf != []:
                res += f'{num}-{num+counter}) ' if counter != 0 else f'{num}) '
                for l in buf:
                    res += f'{l["subject"]} / '
                    res += f'{l["teacher"]} / '
                    res += f'{l["place"]}\n'
            buf = lesson
            num += counter + 1
            counter = 0
    num += 1


    return res


'''
Состоавляет ответ на запрос расписание 
Возвращает: расписание в читаемом виде 
'''
def build_answer(schedule: dict) -> str:
    days = ('Понедельник', 'Вторник', 'Среда', 'Четверг' ,'Пятница' ,'Суббота')

    res = ''

    i = 0
    while i < len(days):
        res += f'\n{days[i]}:\n'
        res += build_day(schedule[i])
        i += 1

    return res