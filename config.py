import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Load environment variables from .env file
TG_TOKEN = os.getenv("TG")
OR_API_KEY = os.getenv("OPENROUTER_API_KEY")
DB_URL = os.getenv("DB_SUPABASE")

