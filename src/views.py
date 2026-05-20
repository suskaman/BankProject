import logging
import datetime
import os
import collections as col
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

    views_logger.info('START getting date for greeting')
    try:
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
    finally:
        views_logger.info('END getting date for greeting')


def get_info_about_all_cards(operations: list[dict]):
    """get the latest 4 digits of card, total expenses, cashback(1 for every 100)"""
    cards = {'cards': []}
    list_of_cards = [operation.get('Номер карты', '') for operation in operations]
    count = dict(col.Counter(list_of_cards))
    keys = count.keys()

    return keys


def get_top_five_transactions(operations: list[dict], date_time: str) -> dict:
    """get five transactions with the largest amount."""
    views_logger.info('START getting top five transactions')
    try:
        if not isinstance(operations, list):
            raise TypeError('operations must be a list')
        if not isinstance(date_time,str):
            raise TypeError('date_time must be of type str')

        top_transactions = {'top_transactions': []}
        # filter data by date
        date = date_time.split(" ")[0]
        month = date.split(".")[1]
        day = date.split(".")[0]
        year = date.split(".")[2]
        year_operations = [operation for operation in operations if operation.get('Дата операции', '').split(" ")[0].split('.')[2] == year]
        month_operations = [operation for operation in year_operations if operation.get('Дата операции', '').split(" ")[0].split('.')[1] == month]
        days_operations = [operation for operation in month_operations if int(operation.get('Дата операции', '').split(" ")[0].split('.')[0]) <= int(day)]
        sorted_by_amount = sorted(days_operations, key=lambda x: x.get('Сумма операции с округлением' , ''), reverse=True)
        top_five = sorted_by_amount[:5]

        for operation in top_five:
            top_transactions['top_transactions'].append({
                "date": operation.get('Дата платежа'),
                "amount": operation.get('Сумма операции с округлением'),
                "category": operation.get('Категория'),
                "description": operation.get('Описание')
            })

    except TypeError as e:
        views_logger.error(f'ERROR: {e}')
        return {}

    finally:
        views_logger.info('END getting top five transactions')

    return top_transactions


def get_exchange_rate(currencies: list) -> dict:
    """get exchange rate.
    USD and EUR"""
    views_logger.info('START getting exchange rate')
    currency_rates = {"currency_rates": []}
    try:
        for currency in currencies:
            url = f'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol={currency}&to_symbol=RUB&apikey={api_alpha}'
            response = requests.get(url)
            data = response.json()
            status = response.status_code
            if status == 200:
                rate = data

                currency_rates["currency_rates"].append({
                "currency": currency,
                "rate": rate,
                })
                time.sleep(1)

    finally:
       views_logger.info('END getting exchange rate')
    return currency_rates


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


def json_home_page(date=''):
    setup = get_data_from_json('C:/Users/maks/PycharmProjects/BankProject/user_settings.json')
    operations = get_data_from_excel('C:/Users/maks/PycharmProjects/BankProject/data/operations.xlsx')

    # 1 greeting
    # home = {"greeting": get_date_for_greeting()}

    # 2 cards info
    cards = get_info_about_all_cards(operations)
    # 3 top 5 transactions
    # home.update(get_top_five_transactions(operations, date))
    # 4 currency rate
    # home.update(get_exchange_rate(setup['user_currencies']))

    # 5 stoke prices
    home.update(get_stoke_prices(setup['user_stocks']))

    return cards
