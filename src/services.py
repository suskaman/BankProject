import collections as col
import json
import logging
import math

services_logger = logging.getLogger("services_logger")


def get_categories_with_profitable_cashback(data: list[dict], year: str, month: str):
    """getting profitable cashback categories list"""

    profitable_categories = {}

    year_operations = [
        operation
        for operation in data
        if operation.get("Дата операции", "").split(" ")[0].split(".")[2] == year
    ]
    month_operations = [
        operation
        for operation in year_operations
        if operation.get("Дата операции", "").split(" ")[0].split(".")[1] == month
    ]

    category_from_operations = [
        operation.get("Категория")
        for operation in month_operations
        if operation.get("Категория")
    ]
    count_of_category = dict(col.Counter(category_from_operations))

    for key in count_of_category.keys():
        if isinstance(key, str):
            sum_of_cashback = sum(
                operation.get("Кэшбэк", 0)
                for operation in month_operations
                if operation.get("Категория") == key
                and not math.isnan(operation.get("Кэшбэк", 0))
            )

            if sum_of_cashback == 0:
                continue

            profitable_categories[key] = sum_of_cashback

    return json.dumps(profitable_categories, ensure_ascii=False, indent=4)


def investment_bank(date: str, transactions: list[dict], limit: int) -> float:
    """calculating a potential amount that could be invested to investment bank"""

    month = date.split("-")[1]
    year = date.split("-")[0]

    year_operations = [
        operation
        for operation in transactions
        if operation.get("Дата операции", "").split(" ")[0].split(".")[2] == year
    ]
    month_operations = [
        operation
        for operation in year_operations
        if operation.get("Дата операции", "").split(" ")[0].split(".")[1] == month
    ]

    potential_earnings = sum(
        (
            math.ceil(operation.get("Сумма операции с округлением", 0) / limit) * limit
            - operation.get("Сумма операции с округлением", 0)
        )
        for operation in month_operations
        if operation.get("Сумма операции с округлением")
    )

    return round(potential_earnings, 2)
