
import asyncio
from openai import AsyncOpenAI

from config import OR_API_KEY




client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OR_API_KEY,
)



async def generate_ai_router(text: str):
  completion = await client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
      messages=[
        {
          "role": "user",
          "content": text
        }
      ]
  )
  print(completion)
  return completion.choices[0].message.content


