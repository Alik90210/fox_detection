
import requests
import json
from roboflow import Roboflow
import config
from aiogram import Bot, types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.utils import executor
import base64
from PIL import Image
from io import BytesIO


bot = Bot(token=config.tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Вставь URL фото")


@dp.message_handler()
async def find_fox(message: types.Message):

    try:
        rf = Roboflow(api_key=config.api_key)
        project = rf.workspace().project("fox_pic")
        model = project.version(2).model

        # infer on an image hosted elsewhere
        predictions = model.predict(message.text, hosted=True, confidence=70, overlap=30).json()

        await message.reply(predictions)

    except Exception as e:
        await message.reply(e)
        await message.reply("\U00002620 check URL \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
