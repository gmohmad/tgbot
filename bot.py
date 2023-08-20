import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor

bot = Bot(token='your_bot_token')
dp = Dispatcher(bot, storage=MemoryStorage())
TEXT, PHOTO = '', ''


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

    btn1 = types.InlineKeyboardButton('Yes', callback_data='btn1')
    btn2 = types.InlineKeyboardButton('No', callback_data='btn2')
    inline_kb1 = types.InlineKeyboardMarkup().add(btn1, btn2)

    global TEXT, PHOTO

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
            "X-API-KEY": "your_API_key"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.json()['image_urls']:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await message.answer("Here's your photo.")
            await bot.send_photo(chat_id=message.chat.id, photo=response.json()['image_urls'][0])
        else:
            photo = requests.post('https://stablediffusionapi.com/api/v3/text2img', data={
                "key": "your_API_key",
                "prompt": f'a detailed isometric flat design vector illustration of {message.text}',
                "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), "
                                   "((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), "
                                   "((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), "
                                   "((bad proportions)), ((extra limbs)), cloned face, (((skinny))), "
                                   "glitchy, ((extra breasts)), ((double torso)), ((extra arms)), "
                                   "((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), "
                                   "((ugly face)), ((fat)), ((extra legs)), anime",
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
            print(photo.text)
            TEXT, PHOTO = text, photo.json()['output'][0]

            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

            if len(text) <= 200:
                await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0], caption=text)
                await message.answer('Send messages to the channel?', reply_markup=inline_kb1)
                pass
            else:
                await bot.send_message(chat_id=message.chat.id, text=text, parse_mode='HTML')
                await bot.send_photo(chat_id=message.chat.id, photo=photo.json()['output'][0])
                await message.answer('Send messages to the channel?', reply_markup=inline_kb1)

    except Exception:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await message.answer('Something went wrong...\n'
                             'Try again later.')


@dp.callback_query_handler(lambda c: c.data == 'btn1' or c.data == 'btn2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code == '1':
        if len(TEXT) <= 200:
            await bot.send_photo(chat_id='your_channel_id', photo=PHOTO, caption=TEXT)
        else:
            await bot.send_message(chat_id='your_channel_id', text=TEXT, parse_mode='HTML')
            await bot.send_photo(chat_id='your_channel_id', photo=PHOTO)

        await callback_query.answer('Done! ✅')
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
    else:
        await callback_query.answer("Ok")
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


executor.start_polling(dp)
