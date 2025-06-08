# 🤖 Проект Telegram-бота "Kiberded"

## 📌 Цель проекта

Бот **Kiberded** — это персональный AI-учитель в Telegram, обучающий пользователей по запросу, выдающий задания, проверяющий ответы, анализирующий прогресс и взаимодействующий через текст, голос и изображения. Поддерживает локализацию, AI-провайдеров, оплату и экспорт отчётов.

---

## ⚙️ Архитектура проекта `kiberded/`

```
kiberded/
├── bot.py                   # точка входа бота
├── config.py                # загрузка переменных окружения
├── database.py              # работа с Supabase и SQLite
├── ai_utils.py              # универсальный интерфейс для AI-провайдеров
├── localization.py          # локализация на основе gettext
├── pdf_exporter.py          # генерация PDF
│
├── core/
│   ├── exceptions.py        # кастомные исключения
│   ├── constants.py         # глобальные константы (лимиты, роли, статусы)
│   └── logging_config.py    # централизованная настройка логирования
│
├── handlers/
│   ├── start.py
│   ├── lessons.py
│   ├── homework.py
│   ├── reminders.py
│   ├── export.py
│   ├── settings.py
│   └── payments.py
│
├── models/
│   ├── user.py
│   ├── lesson.py
│   ├── task.py
│   ├── voice_message.py
│   ├── payment.py
│   └── ai_model.py          # Enum-провайдеров и уровней моделей
│
├── services/
│   ├── check_homework.py
│   ├── generate_tasks.py
│   ├── pdf_service.py
│   ├── ocr_service.py
│   ├── tts_service.py
│   ├── stt_service.py
│   ├── analytics_service.py
│   └── payment_service.py
│
├── providers/
│   ├── openai_api.py
│   ├── google_gemini.py
│   ├── yandex_gpt.py
│   ├── mistral_api.py
│   └── llama_api.py
│
├── templates/
│   └── report.html
│
├── utils/
│   ├── scheduler.py
│   └── token_counter.py
│
├── locales/
│   ├── en/LC_MESSAGES/messages.mo
│   └── ru/LC_MESSAGES/messages.mo
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── .env
└── .env.example
```

---

## 🎯 Основной функционал

* Объяснение тем по запросу (с выбором языка)
* Генерация и выдача практических заданий
* Приём ответов в текстовом, голосовом и графическом виде
* Проверка и оценка ДЗ через AI API (с комментариями и оценками)
* Распознавание текста (OCR) и голосовых сообщений (STT)
* Озвучка объяснений и комментариев (TTS)
* Экспорт всей истории в PDF (по темам или датам)
* Напоминания о задачах (встроенный планировщик)
* Поддержка платных и бесплатных AI моделей
* Многоязычный интерфейс (русский/английский)
* Telegram-only уведомления

---

## 🛢️ Структура базы данных (Supabase/PostgreSQL)

### Таблица `users`

| Поле         | Тип       | Описание             |
| ------------ | --------- | -------------------- |
| id           | UUID      | ID пользователя      |
| telegram\_id | BIGINT    | Telegram ID          |
| language     | TEXT      | язык (ru/en)         |
| created\_at  | TIMESTAMP | дата регистрации     |
| model\_tier  | TEXT      | бесплатный / платный |

### Таблица `lessons`

| Поле        | Тип       | Описание                   |
| ----------- | --------- | -------------------------- |
| id          | UUID      | ID темы                    |
| user\_id    | UUID      | внешний ключ               |
| title       | TEXT      | название темы              |
| content     | TEXT      | сгенерированное объяснение |
| created\_at | TIMESTAMP | дата                       |

### Таблица `tasks`

| Поле        | Тип       | Описание      |
| ----------- | --------- | ------------- |
| id          | UUID      | ID задания    |
| lesson\_id  | UUID      | внешний ключ  |
| content     | TEXT      | текст задания |
| created\_at | TIMESTAMP | дата          |

### Таблица `homework_submissions`

| Поле        | Тип       | Описание                 |
| ----------- | --------- | ------------------------ |
| id          | UUID      | ID ответа                |
| user\_id    | UUID      | внешний ключ             |
| task\_id    | UUID      | внешний ключ             |
| content     | TEXT      | текст/распознанный текст |
| grade       | TEXT      | оценка AI                |
| feedback    | TEXT      | AI комментарий           |
| created\_at | TIMESTAMP | дата ответа              |

### Таблица `payments`

| Поле        | Тип       | Описание           |
| ----------- | --------- | ------------------ |
| id          | UUID      | ID платежа         |
| user\_id    | UUID      | внешний ключ       |
| amount      | NUMERIC   | сумма              |
| provider    | TEXT      | Stripe/ЮKassa и др |
| status      | TEXT      | success/pending    |
| created\_at | TIMESTAMP | дата               |

---

## 🧰 Используемые технологии

* Python 3.11+
* aiogram 3
* PostgreSQL (Supabase)
* SQLite (локально)
* SQLAlchemy + asyncpg
* Pydantic v2
* OpenAI API, Google Gemini API, YandexGPT, Mistral
* gTTS / ElevenLabs / Coqui (для TTS)
* Whisper / Google STT (для расшифровки)
* pdfkit / WeasyPrint для PDF
* gettext + babel — локализация
* pytest, httpx — тестирование
* python-dotenv
* loguru

---

## 🔐 Пример `.env.example`

```env
BOT_TOKEN=your_telegram_token
OPENAI_API_KEY=...
GEMINI_API_KEY=...
DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname
DEBUG=true
DEFAULT_LANGUAGE=ru
PDF_RENDERER=weasyprint
```

---

## 💳 Монетизация и лимиты

* Бесплатный доступ — ограниченное число AI-запросов в сутки (на основе token\_counter)
* Подписка (Pro) — снятие лимитов + доступ к более сильным моделям
* Поддержка Stripe и ЮKassa
* Учёт расходов по каждому пользователю и сессии

---

## 🚧 Этапы реализации

1. **Проектирование архитектуры и базы данных**
2. **Создание базового Telegram-бота и локализации**
3. **Реализация объяснений и генерации заданий через AI**
4. **Обработка входящих текстов, изображений (OCR), голосов (STT)**
5. **Реализация проверки ДЗ, оценка и обратная связь**
6. **Добавление экспорта PDF и напоминаний**
7. **Интеграция TTS и выбор модели AI**
8. **Подключение платёжной системы и лимитов**
9. **Развёртывание в продакшн + Supabase**

---

## 📚 Пример кода: Проверка домашнего задания через AI

```python
# services/check_homework.py
from ai_utils import AIClient

def check_homework(user_id: str, answer_text: str, task_prompt: str) -> dict:
    ai = AIClient.for_user(user_id)
    review = ai.evaluate_homework(answer=answer_text, task=task_prompt)
    return {
        "grade": review["grade"],
        "feedback": review["feedback"]
    }
```

---

## 🛠 Инструкция по запуску в VS Code

1. Установите зависимости:

```
pip install -r requirements.txt
```

2. Скопируйте `.env.example` в `.env` и заполните
3. Запустите бота:

```
python kiberded/bot.py
```

4. Для запуска тестов:

```
pytest
```

5. Для автоформатирования:

```
black . && isort .
```

---

