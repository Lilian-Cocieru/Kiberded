
# C:\Users\Computer\Desktop\python\Kiberded\config.py

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
TG_TOKEN = os.getenv("TEST_BOT_TOKEN")
OR_API_KEY = os.getenv("TEST_OPENROUTER_API_KEY")
