from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu():
    buttons = [
        [KeyboardButton(text="Top 15 States")],
        [KeyboardButton(text="Northeast"), KeyboardButton(text="Midwest")],
        [KeyboardButton(text="South"), KeyboardButton(text="West")],
        [KeyboardButton(text="Mid-Atlantic")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
