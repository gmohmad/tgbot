from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
import requests

bot = Bot(token='6273491081:AAEBVJ2paplE3C4KZE3fNT6qpsRk_YPW7bk')
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
    try:

        url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
        payload = {
            "enable_google_results": True,
            "enable_memory": False,
            "input_text": message.text
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": "cd85b43a-ad30-4732-8e23-4afb43983e72"
        }

        response = requests.post(url, json=payload, headers=headers)
        text = response.json()['message']


        if response.json()['image_urls']:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await bot.send_photo(chat_id=message.chat.id, photo=response.json()['image_urls'][0])
        else:
            photo = requests.post('https://stablediffusionapi.com/api/v3/text2img', data={
                "key": "emjh65FFSdStgAObHVSH3dDCcvOpRRgnLcx9EZz4gqm46wmFd73tLzvneQiv",
                "prompt": message.text + ', drawing style, detailed, hd, cartoon style, realism'
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
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await message.answer(text)
            await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0])

    except Exception:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await message.answer('Something went wrong...\n'
                             'Try again later.')


executor.start_polling(dp)
