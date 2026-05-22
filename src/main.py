import logging

from configurate.logging_config import setup_logging
from src.views import json_home_page
from utils import get_data_from_excel

# create logger
main_logger = logging.getLogger("main")


def main() -> None:
    """The program's main function. Responsible for initializing the application,
    parsing command-line arguments,and starting the program's main loop."""
    operations = get_data_from_excel('../data/operations.xlsx')
    date = "21.12.2021 16:44:00"
    # data = json_home_page(date)
    print(operations[:5])
    return None


if __name__ == "__main__":
    setup_logging()
    main()
