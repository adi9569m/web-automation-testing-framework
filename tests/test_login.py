"""Pytest test cases for login validation."""

import os
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Add the project root to Python path so local imports work reliably.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.config import Config
from pages.login_page import LoginPage


@pytest.fixture
def driver():
    """Set up and tear down the Chrome browser for each test."""
    print("\nLaunching Chrome browser for test execution.")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")

    web_driver = webdriver.Chrome(service=Service(), options=chrome_options)
    web_driver.implicitly_wait(2)

    yield web_driver

    print("Closing Chrome browser after test execution.")
    web_driver.quit()


def test_valid_login(driver):
    """Verify that a user can log in with valid credentials."""
    print("Executing valid login test.")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

    assert login_page.is_products_page_displayed(), (
        "Valid login failed. The products page was not displayed."
    )


def test_invalid_login(driver):
    """Verify that an error appears for invalid credentials."""
    print("Executing invalid login test.")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(Config.INVALID_USERNAME, Config.INVALID_PASSWORD)

    error_message = login_page.get_error_message()
    assert "Username and password do not match" in error_message, (
        f"Unexpected error message displayed: {error_message}"
    )


def test_empty_field_validation(driver):
    """Verify that validation appears when login is submitted with empty fields."""
    print("Executing empty field validation test.")
    login_page = LoginPage(driver)
    login_page.open()
    login_page.click_login()

    error_message = login_page.get_error_message()
    assert "Username is required" in error_message, (
        f"Unexpected validation message displayed: {error_message}"
    )
