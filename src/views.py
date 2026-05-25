import collections as col
import datetime
import json
import logging
import os
import time
from typing import Any

import finnhub  # type: ignore
import requests
from dotenv import load_dotenv

from configurate.logging_config import setup_logging
from src.utils import get_data_from_excel, get_data_from_json

load_dotenv()
api_alpha = os.getenv("API_ALPHA")
api_fin = os.getenv("API_FIN")
views_logger = logging.getLogger("views")


def get_date_for_greeting() -> str:
    """get a present time for greeting.
    06:00–11:59 - Good morning
    12:00–17:59 - Good afternoon
    18:00–22:59 - Good evening
    23:00–05:59 - Good night"""

    views_logger.info("START getting date for greeting")
    try:
        date = datetime.datetime.now()
        time_now = str(date.time())
        hour = int(time_now.split(":")[0])

        if 6 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"

        return greeting

    finally:
        views_logger.info("END getting date for greeting")


def get_info_about_all_cards(operations: list[dict]) -> dict:
    """get the latest 4 digits of card, total expenses, cashback(1 for every 100)"""
    views_logger.info("START getting info about all cards")
    try:
        if operations is None:
            raise ValueError("operations can not be None")
        if not isinstance(operations, list):
            raise TypeError("operations must be a list")

        cards: dict[str, Any] = {"cards": []}
        list_of_cards = [operation.get("Номер карты", "") for operation in operations]
        count = dict(col.Counter(list_of_cards))
        for key in count.keys():
            if isinstance(key, str):
                var = sum(
                    operation.get("Сумма операции с округлением", 0)
                    for operation in operations
                    if operation.get("Номер карты") == key
                )
                cards["cards"].append(
                    {
                        "last_digits": key[1:],
                        "total": round(var, 2),
                        "cashback": round(var / 100, 2),
                    }
                )
        return cards

    except TypeError as e:
        views_logger.error(f"ERROR: {e}")
        return {}
    except ValueError as e:
        views_logger.error(f"ERROR: {e}")
        return {}

    finally:
        views_logger.info("END getting info about all cards")


def get_top_five_transactions(operations: list[dict]) -> dict:
    """get five transactions with the largest amount."""
    views_logger.info("START getting top five transactions")
    try:
        if not isinstance(operations, list):
            raise TypeError("operations must be a list")
        if operations is None:
            raise ValueError("operations can not be None")

        top_transactions: dict[str, Any] = {"top_transactions": []}
        # filter data by date

        sorted_by_amount = sorted(
            operations,
            key=lambda x: x.get("Сумма операции с округлением", ""),
            reverse=True,
        )
        top_five = sorted_by_amount[:5]

        for operation in top_five:
            top_transactions["top_transactions"].append(
                {
                    "date": operation.get("Дата платежа"),
                    "amount": operation.get("Сумма операции с округлением"),
                    "category": operation.get("Категория"),
                    "description": operation.get("Описание"),
                }
            )

    except TypeError as e:
        views_logger.error(f"ERROR: {e}")
        return {}
    except ValueError as e:
        views_logger.error(f"ERROR: {e}")
        return {}

    finally:
        views_logger.info("END getting top five transactions")

    return top_transactions


def get_exchange_rate(currencies: list) -> dict:
    """get exchange rate.
    USD and EUR"""
    views_logger.info("START getting exchange rate")

    try:
        if not isinstance(currencies, list):
            raise TypeError("currencies must be a list")
        if currencies is None:
            raise ValueError("currencies can not be None")

        currency_rates: dict = {"currency_rates": []}
        for currency in currencies:
            url = (
                f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
                f"from_currency={currency}&to_currency=RUB&apikey={api_alpha}"
            )
            response = requests.get(url)
            data = response.json()
            response.raise_for_status()

            rate = round(
                float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]),
                2,
            )
            currency_rates["currency_rates"].append(
                {
                    "currency": currency,
                    "rate": rate,
                }
            )
            time.sleep(1)

        return currency_rates

    except TypeError as e:
        views_logger.error(f"ERROR: {e}")
        return {}
    except ValueError as e:
        views_logger.error(f"ERROR: {e}")
        return {}
    except requests.exceptions.HTTPError as http_err:
        views_logger.error(f"HTTP ошибка: {http_err}")
        return {}
    except requests.exceptions.ConnectionError:
        views_logger.error("Ошибка сети: проверьте подключение к интернету.")
        return {}
    except requests.exceptions.Timeout:
        views_logger.error("Таймаут: сервер не ответил вовремя.")
        return {}

    finally:
        views_logger.info("END getting exchange rate")


def get_stoke_prices(stocks: list) -> dict:
    """get shares price by SPX."""
    views_logger.info("START getting stokes prices")
    try:
        if stocks is None:
            raise ValueError("stocks cannot be None")
        if not isinstance(stocks, list):
            raise TypeError("stocks must be a list")

        finnhub_client = finnhub.Client(api_key=api_fin)
        stock_prices: dict[str, Any] = {"stock_prices": []}
        for stock in stocks:
            price = finnhub_client.quote(stock).get("c")
            stock_prices["stock_prices"].append({"stock": stock, "price": price})

        return stock_prices

    except TypeError as e:
        views_logger.error(f"ERROR: {e}")
        return {}
    except ValueError as e:
        views_logger.error(f"ERROR: {e}")
        return {}

    finally:
        views_logger.info("END getting stokes prices")


def get_operations_by_date(operations: list[dict], date: str) -> list[dict]:
    """filter list of operations by date. from a first day of month to a day by date"""
    views_logger.info("START getting operations by date")
    try:
        if not operations:
            raise ValueError("operations cannot be empty")
        if not isinstance(operations, list):
            raise TypeError("operations must be a list")
        if not isinstance(date, str):
            raise TypeError("date must be a string")
        if date == "":
            raise ValueError("date cannot be empty")

        date = date.split(" ")[0]
        month = date.split(".")[1]
        day = date.split(".")[0]
        year = date.split(".")[2]

        year_operations = [
            operation
            for operation in operations
            if operation.get("Дата операции", "").split(" ")[0].split(".")[2] == year
        ]
        month_operations = [
            operation
            for operation in year_operations
            if operation.get("Дата операции", "").split(" ")[0].split(".")[1] == month
        ]
        days_operations = [
            operation
            for operation in month_operations
            if int(operation.get("Дата операции", "").split(" ")[0].split(".")[0])
            <= int(day)
        ]

        return days_operations

    except TypeError as e:
        views_logger.error(f"ERROR: {e}")
        return [{}]
    except ValueError as e:
        views_logger.error(f"ERROR: {e}")
        return [{}]

    finally:
        views_logger.info("END getting operations by date")


def json_home_page(date: str):
    """main function which get returns from functions and return json-data"""
    if not isinstance(date, str) or date == "":
        date = str(datetime.datetime.now())

    setup = get_data_from_json("../user_settings.json")
    data = get_data_from_excel("../data/operations.xlsx")
    data_by_date = get_operations_by_date(data, date)

    # 1 greeting
    home = {"greeting": get_date_for_greeting()}

    # 2 cards info
    home.update(get_info_about_all_cards(data_by_date))
    # 3 top 5 transactions
    home.update(get_top_five_transactions(data_by_date))

    # 4 currency rate
    home.update(get_exchange_rate(setup["user_currencies"]))

    # 5 stoke prices
    home.update(get_stoke_prices(setup["user_stocks"]))

    json_home = json.dumps(home, ensure_ascii=False, indent=4)

    return json_home


if __name__ == "__main__":
    setup_logging()
