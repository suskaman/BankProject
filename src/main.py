import logging

import pandas as pd

from configurate.logging_config import setup_logging
from reports import spending_by_category
from utils import get_data_from_excel

# create logger
main_logger = logging.getLogger("main")


def main() -> None:
    """The program's main function. Responsible for initializing the application,
    parsing command-line arguments,and starting the program's main loop."""

    # date ='21.12.2021 16:44:00'
    # data = json_home_page(date)
    data = get_data_from_excel("../data/operations.xlsx")
    df = pd.DataFrame(data)

    print(spending_by_category(df, "Супермаркеты", "2021-12-21 10:00:00"))

    return None


if __name__ == "__main__":
    setup_logging()
    main()
