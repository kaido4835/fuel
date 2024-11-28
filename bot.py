import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import config
from handlers.base_handlers import router as base_router
from handlers.fuel_parser import router as fuel_router
from handlers.top15_handlers import router as top15_router, save_top_15_states, create_database

# Logging
logging.basicConfig(level=logging.INFO)

# Bot and dispatcher initialization
bot = Bot(token=config.api_key)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

# Registration of routers
dp.include_router(base_router)
dp.include_router(fuel_router)
dp.include_router(top15_router)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/states_northeast", description="Show Northeast states"),
        BotCommand(command="/states_midwest", description="Show Midwest states"),
        BotCommand(command="/states_south", description="Show South states"),
        BotCommand(command="/states_west", description="Show West states"),
        BotCommand(command="/states_mid_atlantic", description="Show Mid-Atlantic states"),
        BotCommand(command="/fuel", description="Get fuel prices"),
        BotCommand(command="/top15", description="Show top 15 states"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Create a database and save the top 15 states
    create_database()
    await save_top_15_states()

    # Setting up commands and launching the bot
    await set_commands(bot)
    logging.info("Starting bot")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
