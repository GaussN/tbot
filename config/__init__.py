from os import getenv

from dotenv import load_dotenv

from .bells import BELLS

load_dotenv()


BOT_TOKEN = getenv('BOT_TOKEN')
PARSING_LINK = 'https://kbp.by/rasp/timetable/view_beta_kbp/?page=stable&cat=group&id=62'


if BOT_TOKEN is None:
    raise SystemExit('Token is not defined')

