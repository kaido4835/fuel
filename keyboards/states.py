from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_keyboard(states):
    buttons = []
    row = []
    for name, abbr in states:
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([KeyboardButton(text="Back")])
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def get_northeast_keyboard():
    states = [
        ("Connecticut", "CT"), ("Maine", "ME"), ("Massachusetts", "MA"), ("New Hampshire", "NH"),
        ("Rhode Island", "RI"), ("Vermont", "VT"), ("New Jersey", "NJ"), ("New York", "NY"),
        ("Pennsylvania", "PA")
    ]
    return create_keyboard(states)


def get_midwest_keyboard():
    states = [
        ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"), ("Kansas", "KS"),
        ("Michigan", "MI"), ("Minnesota", "MN"), ("Missouri", "MO"), ("Nebraska", "NE"),
        ("North Dakota", "ND"), ("Ohio", "OH"), ("South Dakota", "SD"), ("Wisconsin", "WI")
    ]
    return create_keyboard(states)


def get_south_keyboard():
    states = [
        ("Alabama", "AL"), ("Arkansas", "AR"), ("Delaware", "DE"), ("Florida", "FL"),
        ("Georgia", "GA"), ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maryland", "MD"),
        ("Mississippi", "MS"), ("North Carolina", "NC"), ("Oklahoma", "OK"), ("South Carolina", "SC"),
        ("Tennessee", "TN"), ("Texas", "TX"), ("Virginia", "VA"), ("West Virginia", "WV")
    ]
    return create_keyboard(states)


def get_west_keyboard():
    states = [
        ("Alaska", "AK"), ("Arizona", "AZ"), ("California", "CA"), ("Colorado", "CO"),
        ("Hawaii", "HI"), ("Idaho", "ID"), ("Montana", "MT"), ("Nevada", "NV"),
        ("New Mexico", "NM"), ("Oregon", "OR"), ("Utah", "UT"), ("Washington", "WA"),
        ("Wyoming", "WY")
    ]
    return create_keyboard(states)


def get_mid_atlantic_keyboard():
    states = [
        ("New York", "NY"), ("New Jersey", "NJ"), ("Pennsylvania", "PA")
    ]
    return create_keyboard(states)
