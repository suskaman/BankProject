import logging
import datetime
import os
import time
from unittest import result

import finnhub
import requests

from dotenv import load_dotenv
from src.utils import get_data_from_json, get_data_from_excel

load_dotenv()
api_alpha = os.getenv("API_ALPHA")
api_fin = os.getenv("API_FIN")
views_logger = logging.getLogger('views')

def get_date_for_greeting() -> str:
    """get a present time for greeting.
    06:00–11:59 - Good morning
    12:00–17:59 - Good afternoon
    18:00–22:59 - Good evening
    23:00–05:59 - Good night"""
    
    date = datetime.datetime.now()
    time = str(date.time())
    hour = int(time.split(":")[0])

    if 6 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    elif 18 <= hour < 23:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    return greeting


def get_summary_info_about_all_cards():
    """get the latest 4 digits of card, total expenses, cashback(1 for every 100)"""
    pass


def get_transactions_with_the_largest_amount(operations: list[dict]) -> dict:
    """get five transactions with the largest amount."""
    result = {}
    return result


def get_exchange_rate(currencies: list):
    """get exchange rate.
    USD and EUR"""
    currency_rates = {"currency_rates": []}

    for currency in currencies:
        url = f'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol={currency}&to_symbol=RUB&apikey={api_alpha}'
        response = requests.get(url)
        data = response.json()
        # rate = data

        # currency_rates["currency_rates"].append({
        #     "currency": currency,
        #     "rate": rate,
        # })
        # time.sleep(1)

    return data


def get_stoke_prices(stocks: list) -> dict:
    """get shares price by SPX."""
    finnhub_client = finnhub.Client(api_key=api_fin)
    stock_prices = {"stock_prices": []}
    for stock in stocks:
        price = finnhub_client.quote(stock).get('c')
        stock_prices["stock_prices"].append({
            "stock": stock,
            "price": price
        })

    return stock_prices


def json_home_page(date=0):
    setup = get_data_from_json('C:/Users/suska/PycharmProjects/BankProject/user_settings.json')
    operations = get_data_from_excel('C:/Users/suska/PycharmProjects/BankProject/data/operations.xlsx')

    # 1 greeting
    home = {"greeting": get_date_for_greeting()}

    # 2 cards info

    # 3 top 5 transactions
    top_five = get_transactions_with_the_largest_amount(operations)
    # 4 currency rate
    #home.update(get_exchange_rate(setup['user_currencies']))

    # 5 stoke prices
    home.update(get_stoke_prices(setup['user_stocks']))

    return top_five
