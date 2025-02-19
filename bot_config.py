from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Database

ADMINS = [995712956, ]
# token = dotenv_values(".env")["BOT_TOKEN"]

token = config('TOKEN')

bot = Bot(token=token)
storage = MemoryStorage()
database = Database("database.sqlite3")
dp = Dispatcher(bot, storage=storage)
