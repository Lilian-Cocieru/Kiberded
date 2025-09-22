# C:\Users\Computer\Desktop\python\Kiberded\kb\reply_kb\menu_kb.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Уроки"),
            KeyboardButton(text="📝 Домашка")
        ],
        [
            KeyboardButton(text="📊 Экспорт"),
            KeyboardButton(text="⏰ Напоминания")
        ],
        [
            KeyboardButton(text="⚙️ Настройки")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите пункт меню"
)

# Меню настроек
settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌐 Язык"),
            KeyboardButton(text="🤖 AI-модель")
        ],
        [
            KeyboardButton(text="💳 Подписка / Тариф"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите пункт меню"
)




# Подменю Уроки
lessons_menu = ReplyKeyboardMarkup(
    keyboard=[
        [   
            KeyboardButton(text="➕ Добавить урок"),
            KeyboardButton(text="📋 Список уроков")
        ],

        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)