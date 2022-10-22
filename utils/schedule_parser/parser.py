'''
/  イ          (((ヽ
(  ノ           ￣Y  \
|  ( \   (.  /)  |   )
 ヽ ヽ ` (° ‌ʖ ‌°)_ノ  /
     ＼ | ⌒Ｙ⌒ / /
      | ヽ  |   ﾉ／
      ＼トー仝ーイ
       | ミ土彡/
       ) \  ° /
       (  \  / )
       /  / ████████
      // /   \\ \
'''
import requests
from hashlib import md5

from loguru import logger
from bs4 import BeautifulSoup, Tag 
from fake_useragent import UserAgent


class ScheduleParser:
    def __init__(self, url: str):
        self.__days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
        self.__url = url
        self.__schedule = dict()
        self.__schedule_sum = ''

    @logger.catch
    def __get(self) -> str:
        '''
        Получение страницы с расписанием 
        '''
        page = requests.get(self.__url, headers={'User-Agent': UserAgent().chrome})
        page_soup = BeautifulSoup(page.text, features='html.parser')
        return page_soup
        


    @logger.catch
    def __parse_div(self, div: Tag, *, added: bool = False):
        '''
        Парсинг блока с информацией о паре 
        added - истина если пара - замена
        возвращает: словарь с информацией о паре 
        '''
        lesson = dict()

        lesson['added'] = added 
        lesson['subject'] = div.find('div', {'class': 'subject'}).text
        lesson['teacher'] = div.find('div', {'class': 'teacher'}).text
        lesson['place'] = div.find('div', {'class': 'place'}).text
        lesson['group'] = div.find('div', {'class': 'group'}).text

        return lesson
    
    @logger.catch
    def __parse_td(self, td: Tag) -> list | None:
        '''
        Парсинг блока таблицы с парой(ами)
        is_added - истина если пара - замена 
        возвращает: список пар(пара и её замена;пары по подгруппам;пустой список если нет пары)
        '''
        lessons = list()

        div_all = td.findChildren('div', recursive=False)
        for div in div_all:
            is_added = False
            if 'empty-pair' not in div['class']:
                if 'added' in div['class']: 
                    is_added = True
                lessons.append(self.__parse_div(div, added=is_added))

        #проверка на замену уже записанной пары
        if 2 <= len(lessons) and lessons[1]['added'] and not lessons[0]['added']:
            del lessons[0] # удаление пары вместо которой замена  
        # наверное это очень плохой способ 

        return lessons

    @logger.catch
    def __parse_tr(self, tr: Tag) -> list:
        '''
        Парсинг строкрасписания 
        find_all('td')[1:-1]: первый и воследний div - номер пары
        возвращает: список пар(первые, вторые и тд) для всех дней 
        '''
        lessons = []

        td_all = tr.find_all('td')[1:-1] 
        for td in td_all:
            lessons.append(self.__parse_td(td))
        return lessons

    @logger.catch
    def __parse(self, schedule: BeautifulSoup) -> dict:
        '''
        Составляет полное расписание на неделю
        возвращает: словарь(день недели => список пар)
        '''
        schedule_dict = { i: list() for i in range(7) }
        table = schedule.find('table')

        if table is None:
            raise Exception('The page didn\'t contain a timetable')

        tr_all = table.find_all('tr')[2:] # первые 2 строки то дни недели и метка о замене 
        for tr in tr_all:
            lessons = self.__parse_tr(tr)

            # hardcode
            schedule_dict[0].append(lessons[0])
            schedule_dict[1].append(lessons[1])
            schedule_dict[2].append(lessons[2])
            schedule_dict[3].append(lessons[3])
            schedule_dict[4].append(lessons[4])
            schedule_dict[5].append(lessons[5])
        
        return schedule_dict 

    @logger.catch
    def get_schedule(self, day: int = None) -> dict:
        '''
        Проверяет актуально ли расписание
        Если да, то возвращает его
        Если нет, то парсит актуальное и ⤴
        '''
        if day is not None:
            day = day % 6 
        
        new_schedule = self.__get()
        new_schedule_sum = md5(new_schedule.text.encode()).hexdigest()
         
        if new_schedule_sum != self.__schedule_sum:
            logger.debug('new schedule')
            self.__schedule_sum = new_schedule_sum
            self.__schedule = self.__parse(new_schedule)

        return self.__schedule if day is None else self.__schedule[day]


if __name__ == '__main__':
    PARSING_LINK = 'https://kbp.by/rasp/timetable/view_beta_kbp/?page=stable&cat=group&id=62'
    a = ScheduleParser(PARSING_LINK)
    sch = a.get_schedule()
    
    import json
    json.dump(sch, open('json1.json', 'w+', encoding='utf-8'), ensure_ascii=False)
    
    print(sch, end='\n\n\n')