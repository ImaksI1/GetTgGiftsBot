import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

bot = Bot("8099195869:AAGqNU85844BOFyNMsfoUgdD6W-Z8b5QMDw")
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    gifts = await bot.get_available_gifts()
    for gift in gifts:
        name, gift_list = gift
        print("Name:", name)
        for g in gift_list:
            print(f"Gift ID: {g.id}")
            print(f"Gift Count: {g.remaining_count}")
            if g.sticker.type == 'custom_emoji':
                await message.answer(g.sticker.emoji)
            else:
                await bot.send_sticker(chat_id=message.from_user.id, sticker=g.sticker.file_id)

async def updater():
    while True:
        gifts = await bot.get_available_gifts()
        for gift in gifts:
            name, gift_list = gift
            print("Name:", name)
            for g in gift_list:
                print(f"Gift ID: {g.id}")
                print(f"Gift Count: {g.remaining_count}")
                if g.remaining_count != None:
                    if g.sticker.type == 'custom_emoji':
                        await bot.send_message(chat_id=-1002721617802, text=g.sticker.emoji)
                    else:
                        await bot.send_sticker(chat_id=-1002721617802, sticker=g.sticker.file_id)
        await asyncio.sleep(15)


async def main():
    asyncio.create_task(updater())
    await dp.start_polling(bot)


if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())