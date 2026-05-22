import datetime
import pytest

from views import *


def test_get_date_for_greeting(mocker):
    mock_now = mocker.patch('views.datetime.datetime')
    mock_now.return_value = '2026-05-22 09:00:00'

    function = get_date_for_greeting()
    expect = 'Доброе утро'
    assert function == expect


def test_get_info_about_all_cards():
    function = get_info_about_all_cards()
    expect = 0
    assert function == expect


def test_get_top_five_transactions():
    function = get_top_five_transactions()
    expect = 0
    assert function == expect


def test_get_exchange_rate():
    function = get_exchange_rate()
    expect = 0
    assert function == expect


def test_get_stoke_prices():
    function = get_stoke_prices()
    expect = 0
    assert function == expect


def test_get_days_by_date():
    function = get_days_by_date()
    expect = 0
    assert function == expect
