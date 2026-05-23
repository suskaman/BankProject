from src.services import get_categories_with_profitable_cashback, investment_bank

def test_get_categories_with_profitable_cashback(data_for_services, categories_with_profitable_cashback):
    assert (get_categories_with_profitable_cashback(data_for_services, '2021', '01') ==
            categories_with_profitable_cashback)

def test_investment_bank(data_for_services):
    assert investment_bank("2021-01", data_for_services, 50) == 84