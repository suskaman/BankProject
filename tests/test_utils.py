from src.utils import get_data_from_excel, get_data_from_json


def test_get_data_from_excel():
    assert type(get_data_from_excel("../BankProject/data/operations.xlsx")) == list
    assert get_data_from_excel("../BankProject/data/operations.xlsx") != [{}]


def test_get_data_from_json():
    assert type(get_data_from_json("../BankProject/user_settings.json")) == dict
    assert get_data_from_json("../BankProject/user_settings.json") != {}
