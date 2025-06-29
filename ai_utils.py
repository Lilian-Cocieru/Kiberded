




from openai import AsyncOpenAI
import httpx # Важно: добавьте этот импорт
from config import OR_API_KEY

# Инициализация клиента OpenRouter/OpenAI.
# Если проблемы с подключением сохраняются, раскомментируйте строку с http_client.
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1", # Убедитесь, что это корректный base_url для OpenRouter
    api_key=OR_API_KEY,
    # Если проблемы с подключением сохраняются, раскомментируйте эту строку:
    # http_client=httpx.AsyncClient(http2=False)
)

async def ai_generate(text: str, model_code: str) -> str:
    """
    Генерирует ответ от AI-модели на основе заданного текста и кода модели.

    Args:
        text (str): Входной текст пользователя (запрос).
        model_code (str): Код AI-модели для использования (например, "qwen/qwen3-30b-a3b:free").

    Returns:
        str: Сгенерированный ответ от AI.
    """
    try:
        completion = await client.chat.completions.create(
            model=model_code, # Теперь модель передается как аргумент!
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        # print(completion) # Закомментировал вывод всего completion, чтобы не засорять логи
        return completion.choices[0].message.content or ""
    except Exception as e:
        print(f"Ошибка при генерации AI-ответа: {e}")
        # Здесь можно добавить более детальную обработку ошибок,
        # например, логирование или отправку сообщения пользователю.
        raise # Перевыбрасываем ошибку, чтобы её мог обработать хендлер




# from openai import AsyncOpenAI
# from config import OR_API_KEY

# client = AsyncOpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=OR_API_KEY,
# )

# async def ai_generate(text: str):
#   completion = await client.chat.completions.create(
#     # model = "google/gemini-2.5-flash-preview-05-20",
#     model="qwen/qwen3-30b-a3b:free",
#     # model="mistralai/devstral-small:free",
#     # model = "deepseek/deepseek-chat-v3-0324:free",
#     messages=[
#       {
#         "role": "user",
#         "content": text
#       }
#     ]
#   )
#   print(completion)
#   return completion.choices[0].message.content