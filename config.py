
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


DEFAULT_EMBED_MODEL = "local:BAAI/bge-small-en-v1.5"  # Пока оставляем как есть

# Бесплатные модели

MODEL_QWEN = {
    "id": 2,
    "name": "Qwen 3",
    "provider": "OpenRouter",
    "model_code": "qwen/qwen3-30b-a3b:free",
    "is_paid": False,
    "default_limit": 100000,
    "is_active": True
}

MODEL_GEMINI_FLASH = {
    "id": 3,
    "name": "Gemini Flash",
    "provider": "OpenRouter",
    "model_code": "google/gemini-1.5-flash",
    "is_paid": False,
    "default_limit": 100000,
    "is_active": True
}


FREE_MODELS = [MODEL_QWEN, MODEL_GEMINI_FLASH]


# Платные модели

MODEL_GPT4O = {
    "id": 1,
    "name": "GPT-4o",
    "provider": "OpenRouter",
    "model_code": "openai/gpt-4o",
    "is_paid": True,
    "default_limit": 500000,
    "is_active": True
}

# ALL_MODELS = [MODEL_GPT4O]