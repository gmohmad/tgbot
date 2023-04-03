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
            "enable_google_results": False,
            "enable_memory": False,
            "input_text": f'{message.text}. NO LINKS, NO TAGS in your answer.',
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
                "key": "zHIu8P4QLmaXRQbU8ArrgiPQM9WgvonCkUAKTkvwcbg0NrO0TvGqegc4gyrT",
                "prompt": f'a detailed isometric flat design vector illustration of {message.text}',
                "negative_prompt": "",
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

            text = response.json()['message']

            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

            if len(text) <= 200:
                await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0], caption=text)
                pass
            else:
                await bot.send_message(chat_id=message.chat.id, text=text, parse_mode='HTML')
                await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0])

    except Exception:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await message.answer('Something went wrong...\n'
                             'Try again later.')


executor.start_polling(dp)


