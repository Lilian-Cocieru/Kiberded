from openai import AsyncOpenAI
from config import OR_API_KEY

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OR_API_KEY,
)

async def ai_generate(text: str):
  completion = await client.chat.completions.create(
    # model = "google/gemini-2.5-flash-preview-05-20",
    model="qwen/qwen3-30b-a3b:free",
    # model="mistralai/devstral-small:free",
    # model = "deepseek/deepseek-chat-v3-0324:free",
    messages=[
      {
        "role": "user",
        "content": text
      }
    ]
  )
  print(completion)
  return completion.choices[0].message.content