import logging

from services import investment_bank
from utils import get_data_from_excel

from configurate.logging_config import setup_logging
from src.views import json_home_page
from src.services import get_categories_with_profitable_cashback

# create logger
main_logger = logging.getLogger("main")

def main() -> None:
    """The program's main function. Responsible for initializing the application,
    parsing command-line arguments,and starting the program's main loop."""

    # date ='21.12.2021 16:44:00'
    # data = json_home_page(date)
    data = get_data_from_excel('../data/operations.xlsx')
    print(get_categories_with_profitable_cashback(data, '2021', '02'))
    # print(investment_bank('2021-02', data, 10))

    return None


if __name__ == "__main__":
    setup_logging()
    main()
