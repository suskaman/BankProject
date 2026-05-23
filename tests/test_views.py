import pandas as pd

from views import (get_date_for_greeting, get_info_about_all_cards,
                   get_top_five_transactions, get_exchange_rate,
                   get_stoke_prices, get_operations_by_date)


def test_get_date_for_greeting(mocker):
    mock_now = mocker.patch("views.datetime.datetime")
    mock_now.now.return_value = pd.to_datetime("2026-05-22 09:00:00")

    assert get_date_for_greeting() == "Доброе утро"


def test_get_info_about_all_cards(data_for_views: list[dict], info_about_cards: dict):
    assert get_info_about_all_cards(data_for_views) == info_about_cards


def test_get_top_five_transactions(
    data_for_views: list[dict], top_five_transactions: dict
):
    assert get_top_five_transactions(data_for_views) == top_five_transactions


def test_get_exchange_rate(mocker, currency_rates: dict):
    mock_request = mocker.patch("views.requests.get")
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {
        "Realtime Currency Exchange Rate": {
            "5. Exchange Rate": 71,
        }
    }

    assert get_exchange_rate(["USD", "EUR"]) == currency_rates


def test_get_stoke_prices(mocker, finnhub_stock_prices):
    mock_finnhub_client = mocker.patch("views.finnhub.Client")
    mock_finnhub_client.return_value.quote.return_value = {"c": 100}

    assert (
        get_stoke_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
        == finnhub_stock_prices
    )


def test_get_days_by_date(data_for_views: list[dict], filter_by_date: dict):
    assert (
        get_operations_by_date(data_for_views, "21.01.2021 16:44:00") == filter_by_date
    )
