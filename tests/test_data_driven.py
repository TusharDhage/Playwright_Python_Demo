import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_reader import DataReader


def load_csv_data():
    """Load all login data from CSV for parametrize"""
    data = DataReader.read_csv("login_data.csv")
    return [
        (
            row["username"],
            row["password"],
            row["expected_result"],
            row["test_type"]
        )
        for row in data
    ]


def load_excel_valid_data():
    """Load only valid rows from Excel"""
    data = DataReader.read_excel("login_data.xlsx")
    return [
        (row["username"], row["password"], row["expected_result"])
        for row in data
        if row["test_type"] == "valid"
    ]


def load_excel_invalid_data():
    """Load only invalid rows from Excel"""
    data = DataReader.read_excel("login_data.xlsx")
    return [
        (row["username"], row["password"], row["expected_result"])
        for row in data
        if row["test_type"] == "invalid"
    ]


@allure.feature("Data Driven Login")
class TestDataDrivenCSV:

    @allure.story("CSV data driven login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username, password, expected_result, test_type",
        load_csv_data()
    )
    def test_login_with_csv_data(
        self, page, username, password, expected_result, test_type
    ):
        with allure.step(f"Open login page"):
            login = LoginPage(page)
            login.open()

        with allure.step(f"Login as '{username}' — type: {test_type}"):
            login.login(username, password)

        if test_type == "valid":
            with allure.step("Verify successful login"):
                assert expected_result in DashboardPage(page).get_heading()
        else:
            with allure.step("Verify error message"):
                assert expected_result in login.get_error_message()


@allure.feature("Data Driven Login")
class TestDataDrivenExcel:

    @allure.story("Excel data driven — valid login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "username, password, expected_result",
        load_excel_valid_data()
    )
    def test_valid_login_from_excel(
        self, page, username, password, expected_result
    ):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step(f"Login with username: {username}"):
            login.login(username, password)
        with allure.step("Verify dashboard heading"):
            assert expected_result in DashboardPage(page).get_heading()

    @allure.story("Excel data driven — invalid login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username, password, expected_result",
        load_excel_invalid_data()
    )
    def test_invalid_login_from_excel(
        self, page, username, password, expected_result
    ):
        with allure.step("Open login page"):
            login = LoginPage(page)
            login.open()
        with allure.step(f"Login with username: {username}"):
            login.login(username, password)
        with allure.step("Verify error message"):
            assert expected_result in login.get_error_message()