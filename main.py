import logging
import asyncio
from aiogram import Bot
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
bot = Bot(config["DEFAULT"]["BOT_TOKEN"])

async def updater():
    new_gifts_ids = []
    while True:
        gifts = await bot.get_available_gifts()
        for gift in gifts:
            name, gift_list = gift
            print("Name:", name)
            for g in gift_list:
                print(f"Gift ID: {g.id}")
                print(f"Gift Count: {g.remaining_count}")
                if g.remaining_count != None and g.id not in new_gifts_ids:
                    new_gifts_ids.append(g.id)
                    if g.sticker.type == 'custom_emoji':
                        await bot.send_message(chat_id=config["DEFAULT"]["CHAT_ID"], text=g.sticker.emoji)
                    else:
                        await bot.send_sticker(chat_id=config["DEFAULT"]["CHAT_ID"], sticker=g.sticker.file_id)
        await asyncio.sleep(int(config["DEFAULT"]["UPDATER_INTERVAL"]))

async def main():
    await asyncio.create_task(updater())
    await asyncio.Event().wait()

if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())