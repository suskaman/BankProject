import os

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(data_for_reports: pd.DataFrame) -> None:
    result = spending_by_category(
        data_for_reports, "Супермаркеты", "31.12.2021 15:44:39"
    )

    assert len(result) == 2
    assert (result["Категория"] == "Супермаркеты").all().all()
    assert isinstance(result, pd.DataFrame)


def test_create_report_file(data_for_reports: pd.DataFrame) -> None:
    test_file_name = "custom_report.txt"
    spending_by_category(data_for_reports, "Еда", "2024-04-30")

    assert os.path.exists(test_file_name)
