import logging
from functools import wraps
from typing import Callable, Optional

import pandas as pd

report_logger = logging.getLogger("report")


def save_report(filename: Optional[str] = None):
    """save report to file"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)
            file = filename if filename is not None else func.__name__ + ".txt"

            with open(file, "w", encoding="utf-8") as f:
                f.write(result.to_string())

            return result

        return wrapper

    return decorator


@save_report("custom_report.txt")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """return spending by category for the last three months"""
    report_logger.info("START getting spending by category")
    try:
        if not isinstance(transactions, pd.DataFrame):
            raise TypeError("transactions is not a dataframe")
        if not isinstance(category, str):
            raise TypeError("category is not a string")
        if date is not None and not isinstance(date, str):
            raise TypeError("date is not a string")

        if date is None:
            end_date = pd.Timestamp.today()
        else:
            end_date = pd.to_datetime(date)

        start_date = end_date - pd.DateOffset(months=3)
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], dayfirst=True
        )
        spending = transactions[
            (transactions["Категория"] == category)
            & (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
        ]

        return spending

    except TypeError as e:
        report_logger.error(f"ERROR: {e}")
        return pd.DataFrame()

    finally:
        report_logger.info("END getting spending by category")
