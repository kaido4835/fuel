import aiohttp
from bs4 import BeautifulSoup
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import sqlite3
from config import config
import logging
from .fuel_parser import STATES

router = Router()

STATES = STATES

DATABASE = 'fuel_prices.db'


def create_database():
    logging.info("Creating database and table if not exists...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fuel_prices (
            id INTEGER PRIMARY KEY,
            state TEXT NOT NULL,
            price TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


async def parse_fuel_prices(state_code):
    url = f"https://gasprices.aaa.com/?state={state_code}"
    logging.info(f"Fetching data for {state_code} from {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=config.headers) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'lxml')
    try:
        price_block = soup.find("table", class_="table-mob")
        price_table = price_block.find_all("td")[4]
        price_text = price_table.text.strip()
        logging.info(f"Price for {state_code}: {price_text}")
        return price_text
    except Exception as e:
        logging.error(f"Error parsing price for {state_code}: {e}")
        return None


async def save_top_15_states():
    logging.info("Starting to parse and save top 15 states...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    prices = []
    for state_name, state_code in STATES.items():
        price = await parse_fuel_prices(state_code)
        if price is not None:
            prices.append((state_name, price))

    prices.sort(key=lambda x: float(x[1].replace('$', '')))
    top_15_states = prices[:15]

    logging.info("Saving top 15 states to database...")
    cursor.execute('DELETE FROM fuel_prices')
    cursor.executemany('INSERT INTO fuel_prices (state, price) VALUES (?, ?)', top_15_states)
    conn.commit()
    conn.close()
    logging.info("Top 15 states saved successfully.")


@router.message(Command("top15"))
async def send_top_15_states(message: Message):
    logging.info("Fetching top 15 states from database...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT state, price FROM fuel_prices ORDER BY CAST(SUBSTR(price, 2) AS REAL) ASC LIMIT 15')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        response = "\n".join([f"{row[0]}: {row[1]}" for row in rows])
        await message.answer(f"Top 15 States with the lowest fuel prices:\n{response}")
    else:
        await message.answer("No data available.")
        logging.warning("No data available in the database.")


@router.message(lambda message: message.text == "Top 15 States")
async def handle_top_15_button(message: Message):
    logging.info("Fetching top 15 states from database...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT state, price FROM fuel_prices ORDER BY CAST(SUBSTR(price, 2) AS REAL) ASC LIMIT 15')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        response = "\n".join([f"{row[0]}: {row[1]}" for row in rows])
        await message.answer(f"Top 15 States with the lowest fuel prices:\n{response}")
    else:
        await message.answer("No data available.")
        logging.warning("No data available in the database.")

create_database()
