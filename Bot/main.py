# -*- coding: utf-8 -*-
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.client.bot import DefaultBotProperties

import config as cf
from Router_start import router_start


async def main():
    bot = Bot(token = cf.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ChatActionMiddleware())
    dp.include_router(router_start)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
        
