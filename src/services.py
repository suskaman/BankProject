import json
import logging
import collections as col
import math


services_logger = logging.getLogger('services_logger')

def get_categories_with_profitable_cashback(data: list[dict], year: str, month: str):
    """getting profitable cashback categories list"""
    services_logger.info("START getting profitable cashback categories list")
    try:
        if isinstance(data, list):
            raise TypeError("data must be a list")
        if isinstance(year, str):
            raise TypeError("year must be a string")
        if isinstance(month, str):
            raise TypeError("month must be a string")
        if data is None:
            raise ValueError("data cannot be None")
        if year is None:
            raise ValueError("year cannot be None")
        if month is None:
            raise ValueError("month cannot be None")

        profitable_categories = {}
        year_operations = [operation for operation in data if
                           operation.get('Дата операции', '').split(" ")[0].split('.')[2] == year]
        month_operations = [operation for operation in year_operations if
                            operation.get('Дата операции', '').split(" ")[0].split('.')[1] == month]

        category_from_operations = [operation.get('Категория') for operation in month_operations if operation.get('Категория')]
        count_of_category = dict(col.Counter(category_from_operations))

        for key in count_of_category.keys():
            if isinstance(key, str):
                sum_of_cashback = sum(operation.get('Кэшбэк', 0)
                                          for operation in month_operations
                                          if operation.get('Категория') == key
                                          and not math.isnan(operation.get('Кэшбэк', 0)))

                if sum_of_cashback == 0:
                    continue

                profitable_categories[key] = sum_of_cashback

        return json.dumps(profitable_categories, ensure_ascii=False, indent=4)

    except TypeError as e:
        services_logger.error(f"ERROR: {e}")
    except ValueError as e:
        services_logger.error(f"ERROR: {e}")

    finally:
        services_logger.info("END getting profitable cashback categories list")


def investment_bank(date: str, transactions: list[dict], limit: int) -> float:
    """calculating a potential amount that could be invested to investment bank"""
    services_logger.info("START calculation potential amount for investment bank")
    try:
        if isinstance(transactions, list):
            raise TypeError("transactions must be a list")
        if isinstance(date, str):
            raise TypeError("date must be a string")
        if isinstance(limit, int):
            raise TypeError("limit must be a integer")
        if transactions is None:
            raise ValueError("transactions cannot be None")
        if date is None:
            raise ValueError("date cannot be None")
        if limit is None:
            raise ValueError("limit cannot be None")

        month = date.split("-")[1]
        year = date.split("-")[0]

        year_operations = [operation for operation in transactions if
                           operation.get('Дата операции', '').split(" ")[0].split('.')[2] == year]
        month_operations = [operation for operation in year_operations if
                            operation.get('Дата операции', '').split(" ")[0].split('.')[1] == month]

        potential_earnings = sum((math.ceil(operation.get('Сумма операции с округлением', 0)/limit)*limit -
                                 operation.get('Сумма операции с округлением', 0))
                              for operation in month_operations
                              if operation.get('Сумма операции с округлением'))

        return round(potential_earnings, 2)

    except TypeError as e:
        services_logger.error(f"ERROR: {e}")
        return 0
    except ValueError as e:
        services_logger.error(f"ERROR: {e}")
        return 0

    finally:
        services_logger.info("END calculation potential amount for investment bank")
