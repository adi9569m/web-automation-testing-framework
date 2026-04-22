"""Page object for the SauceDemo login page."""

import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class LoginPage:
    """Encapsulates locators and actions for the login page."""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    PRODUCTS_TITLE = (By.CSS_SELECTOR, "span.title")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def open(self) -> None:
        """Open the login page URL."""
        logging.info("Opening application URL: %s", Config.BASE_URL)
        self.driver.get(Config.BASE_URL)

    def _find_element(self, locator: tuple) -> object:
        """Wait for an element to become visible and return it."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException as exc:
            logging.error("Element not visible within timeout: %s", locator)
            raise TimeoutException(f"Timed out waiting for element: {locator}") from exc
        except NoSuchElementException as exc:
            logging.error("Element not found: %s", locator)
            raise NoSuchElementException(f"Element not found: {locator}") from exc

    def enter_username(self, username: str) -> None:
        """Enter a username into the username field."""
        logging.info("Entering username.")
        username_field = self._find_element(self.USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str) -> None:
        """Enter a password into the password field."""
        logging.info("Entering password.")
        password_field = self._find_element(self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self) -> None:
        """Click the login button."""
        logging.info("Clicking the login button.")
        login_button = self._find_element(self.LOGIN_BUTTON)
        login_button.click()

    def login(self, username: str, password: str) -> None:
        """Perform the complete login action."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Return the visible login error message."""
        logging.info("Reading the error message.")
        error_element = self._find_element(self.ERROR_MESSAGE)
        return error_element.text.strip()

    def is_products_page_displayed(self) -> bool:
        """Check whether the user successfully reached the products page."""
        try:
            title = self.wait.until(
                EC.visibility_of_element_located(self.PRODUCTS_TITLE)
            )
            return title.text.strip().lower() == "products"
        except TimeoutException:
            logging.error("Products page was not displayed after login.")
            return False
