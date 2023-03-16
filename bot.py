import re

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor

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
            "input_text": f'my query is: {message.text}, but dont send me any link, only text'
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": "06aeb672-8d49-4ace-9b41-1837b70906b2"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.json()['image_urls']:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await message.answer("Here's your photo.")
            await bot.send_photo(chat_id=message.chat.id, photo=response.json()['image_urls'][0])
        else:
            photo = requests.post('https://stablediffusionapi.com/api/v3/text2img', data={
                "key": "YmnF8ifpCXQ3X6fzGfxtbcFKsmBF2iVWlRP1IzfEDEZKfNYUeoBfE8kVvbGo",
                "prompt": message.text + 'flat style, Flat style, colorfull, 8k',
                "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), \
                                (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, \
                                ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), \
                                ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs))",
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

            brackets = re.compile("\[\d+\]")
            text = brackets.sub('', response.json()['message'])

            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

            if len(text) <= 200:
                await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0], caption=text)
                pass
            else:
                await message.answer((text.replace('<b', '☺', 1)[:text.index('☺')] if '<b' in text else text))
                await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0])

    except Exception:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await message.answer('Something went wrong...\n'
                             'Try again later.')


executor.start_polling(dp)

