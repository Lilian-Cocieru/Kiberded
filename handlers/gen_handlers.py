from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from ai_utils import ai_generate


gen = Router()


class Gen(StatesGroup):
    waiting = State


    
@gen.message(F.state == Gen.waiting)
async def stop_flood(message: Message):
    await message.answer('Подождите, ваш запрос генерируется')
    
    
@gen.message()
async def generating(message: Message, state: FSMContext):
    await state.set_state(Gen.waiting)
    await ai_generate(message.text)
    response = await ai_generate(message.text)
    await message.answer(response) # можно было и так написать (response, parse_mode='Markdown')
    await state.clear()