from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu import get_main_menu
from keyboards.states import (
    get_northeast_keyboard, get_midwest_keyboard, get_south_keyboard,
    get_west_keyboard, get_mid_atlantic_keyboard
)

router = Router()


@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Welcome! Choose a region:", reply_markup=get_main_menu())


@router.message(lambda message: message.text == "Top 15 States")
async def send_top_15_states(message: Message):
    # Need some changes
    top_15_states = [
        "California", "Texas", "Florida", "New York", "Pennsylvania",
        "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan",
        "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts"
    ]
    response = "\n".join(top_15_states)
    await message.answer(f"Top 15 States:\n{response}")


@router.message(lambda message: message.text in ["Northeast", "Midwest", "South", "West", "Mid-Atlantic"])
async def send_region_states(message: Message):
    region = message.text
    if region == "Northeast":
        await message.answer("Choose a state in the Northeast region:", reply_markup=get_northeast_keyboard())
    elif region == "Midwest":
        await message.answer("Choose a state in the Midwest region:", reply_markup=get_midwest_keyboard())
    elif region == "South":
        await message.answer("Choose a state in the South region:", reply_markup=get_south_keyboard())
    elif region == "West":
        await message.answer("Choose a state in the West region:", reply_markup=get_west_keyboard())
    elif region == "Mid-Atlantic":
        await message.answer("Choose a state in the Mid-Atlantic region:", reply_markup=get_mid_atlantic_keyboard())


@router.message(lambda message: message.text == "Back")
async def go_back_to_regions(message: Message):
    await message.answer("Choose a region:", reply_markup=get_main_menu())
