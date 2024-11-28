import requests
import lxml
from bs4 import BeautifulSoup
from aiogram import Router
from aiogram.types import Message
from config import config

router = Router()

STATES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}


async def parse_fuel_prices(state_code):
    url = f"https://gasprices.aaa.com/?state={state_code}"
    data = requests.get(url, headers=config.headers)
    html = data.text
    soup = BeautifulSoup(html, 'lxml')
    try:
        price_block = soup.find("table", class_="table-mob")
        price_table = price_block.find_all("td")[4]
        return price_table.text.strip()
    except Exception as e:
        return "N/A"


@router.message(lambda message: message.text in STATES.keys())
async def process_state_message(message: Message):
    state_name = message.text
    state_code = STATES[state_name]
    price = await parse_fuel_prices(state_code)
    await message.answer(f"Current fuel price in {state_name} ({state_code}): {price}")
