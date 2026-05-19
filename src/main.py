import logging
import pprint

from utils import get_data_from_excel

from configurate.logging_config import setup_logging
from src.views import get_date_for_greeting, get_exchange_rate, json_home_page

# create logger
main_logger = logging.getLogger("main")

def main() -> None:
    """The program's main function. Responsible for initializing the application,
    parsing command-line arguments,and starting the program's main loop."""

    # data = get_data_from_excel("data/operations.xlsx")
    # print(data)
    #
    # date = get_date_for_greeting()
    # print(date)
    date ='31.12.2021 16:44:00'
    data = json_home_page(date)
    pprint.pprint(data, indent=4)
    return None


if __name__ == "__main__":
    setup_logging()
    main()
