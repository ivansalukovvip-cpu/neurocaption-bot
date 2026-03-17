import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import requests

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

HF_TOKEN = "hf_..."  # можешь оставить пустым — многие модели работают без него

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Кидай фото или описание — сделаю тебе 15 вирусных подписей 🔥\n\nПремиум — /premium")

@dp.message(F.photo | F.text)
async def generate(message: types.Message):
    if message.photo:
        await message.answer("Анализирую фото...")
        prompt = "Опиши это фото для OnlyFans/TikTok в одном предложении"
    else:
        prompt = message.text
    
    # Бесплатный вызов нейросети (Hugging Face)
    payload = {"inputs": f"Создай 15 крутых подписей для фото в нише {prompt}. Сделай их вирусными, с эмодзи и призывами к действию."}
    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json=payload
    )
    result = response.json()[0]["generated_text"]
    
    await message.answer(f"✅ Вот твои подписи:\n\n{result}\n\nХочешь больше? Подключи премиум /premium")

@dp.message(Command("premium"))
async def premium(message: types.Message):
    await message.answer("Премиум 299 руб/мес — неограниченные генерации!\nОплата через Telegram Stars (кнопка ниже)")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
