from os import getenv

from dotenv import load_dotenv

from .bells import BELLS


load_dotenv()


BOT_TOKEN = getenv('BOT_TOKEN')
ADMIN_ID = getenv('ADMIN_ID')
GROUP_ID =getenv('GROUP_ID')

PARSING_LINK = 'https://kbp.by/rasp/timetable/view_beta_kbp/?page=stable&cat=group&id=62'
TIMEOUT = 1


if BOT_TOKEN is None:
    raise SystemExit('Token is not defined')

if ADMIN_ID is None:
    raise SystemExit('Admin is not defined')

if GROUP_ID is None:
    raise SystemExit('Group is not defined')