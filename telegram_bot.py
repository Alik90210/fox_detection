
from roboflow import Roboflow
from config import  project_id, model_version, confidence, iou_thresh, api_key, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Вставь URL фото")


@dp.message_handler()
async def find_fox(message: types.Message):

    try:
        rf = Roboflow(api_key=api_key)
        project = rf.workspace().project(project_id)
        model = project.version(model_version).model

        # infer on an image hosted elsewhere
        predictions = model.predict(message.text, hosted=True, confidence=confidence, overlap=iou_thresh).json()

        await message.reply(predictions)

    except Exception as e:
        await message.reply(e)
        await message.reply("\U00002620 check URL \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
