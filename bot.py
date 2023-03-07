from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
import requests

bot = Bot(token='6273491081:AAGHyX18pgOTjSgYilP90CZ-7GjwEPutLCc')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(Command('start'))
async def enter_test(message: types.Message):
    await message.answer('Hi!\n'
                         'This bot will help you stay up-to-date on all the latest happenings in the world.\n'
                         'Just type in what you want to know about and the bot will give you the relevant information.\n'
                         'For more correct answers, enter a detailed query.')


@dp.message_handler()
async def f(message: types.Message):
    await message.answer("Your request is being processed.\n"
                         "It may take about a minute.\n"
                         "Please, be patient...")

    photo = requests.post('https://stablediffusionapi.com/api/v3/text2img', data={
        "key": "CBHpTmwCtDlmWviGVsgk3D6VQuxAySHi9FaU2qfVMIdPNwCrcF2Hb3JBVBmz",
        "prompt": message.text,
        "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), \
                (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, \
                ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), \
                ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs)), anime",
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "webhook": None,
        "track_id": None
    })

    url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
    payload = {
        "enable_google_results": True,
        "enable_memory": False,
        "input_text": message.text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "1a15213e-bd0c-4099-8899-9cccc9aa64ae"
    }

    response = requests.post(url, json=payload, headers=headers)

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

    await message.answer(response.json()['message'])
    await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0])


executor.start_polling(dp)
