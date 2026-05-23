import json
import logging

import pandas as pd

from configurate.logging_config import setup_logging

# create logger
util_logger = logging.getLogger("utils")


def get_data_from_excel(path_to_xlsx: str) -> list[dict]:
    """get data from the xlsx file and return it as a list of dict"""
    util_logger.info("START getting data from excel")

    try:
        df = pd.read_excel(path_to_xlsx)
        util_logger.info("Excel file loaded")
        return df.to_dict(orient="records")

    except FileNotFoundError:
        util_logger.error("invalid file path")
        return [{}]

    except pd.errors.EmptyDataError:
        util_logger.error("EXCEL file is empty")
        return [{}]

    finally:
        util_logger.info("FINISH getting data from excel")


def get_data_from_json(path_to_json: str) -> dict:
    """return a list of all transactions"""
    util_logger.info("START getting transactions")

    try:
        with open(path_to_json, "r", encoding="utf-8") as f:
            util_logger.info("opened json file")

            data = json.load(f)

            util_logger.info("transactions are got")
            return data

    except FileNotFoundError:
        util_logger.error(
            "transactions are not found, please check the path", exc_info=True
        )
        return {}

    except json.decoder.JSONDecodeError:
        util_logger.error("invalid json file", exc_info=True)
        return {}

    except ValueError:
        util_logger.error(
            "json file must contain a list of transactions", exc_info=True
        )
        return {}

    finally:
        util_logger.info("END getting transactions")


if __name__ == "__main__":
    setup_logging()
