from datetime import datetime, timedelta

from loguru import logger

from loader import last_request_time


def check_timeout(*, index_in_lrtl: int, timeout: int = 3) -> bool:
    '''
    log: str
        текст лога
    timeout: int = 
        время таймаута
    index_in_lrtl: int = 0
        индекс в списке last_request_time из loader
    '''
    if datetime.now() <= (last_request_time[index_in_lrtl] + timedelta(minutes=timeout)):
        return False  
    last_request_time[index_in_lrtl] = datetime.now()
        
    return True