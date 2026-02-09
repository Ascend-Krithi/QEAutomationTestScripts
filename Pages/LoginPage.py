# Pages/LoginPage.py

"""
LoginPage PageClass

Implements functions for:
    1. Navigating to the login page
    2. Entering valid/invalid credentials
    3. Clicking the login button
    4. Verifying successful login or error messages

Test Cases Covered:
    - TC01: Valid login
    - TC02: Invalid login

Author: [Your Name]
Date: [YYYY-MM-DD]
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    PageClass representing the Login Page.

    Methods:
        navigate_to_login_page(): Navigates to the login page.
        enter_credentials(username, password): Enters the provided username and password.
        click_login_button(): Clicks the login button.
        is_login_successful(): Verifies if login was successful.
        is_error_message_displayed(): Verifies if error message is displayed.
    """

    # Locators (update as per actual application)
    USERNAME_INPUT = (By.ID, "username-field")
    PASSWORD_INPUT = (By.ID, "password-field")
    LOGIN_BUTTON = (By.ID, "login-btn")
    DASHBOARD_INDICATOR = (By.ID, "dashboard")  # Element present only after successful login
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".login-error-message")  # Element for error messages

    def __init__(self, driver: WebDriver, base_url: str):
        """
        Initializes the LoginPage with the WebDriver and base URL.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            base_url (str): Base URL of the application.
        """
        self.driver = driver
        self.base_url = base_url

    def navigate_to_login_page(self):
        """
        Navigates to the login page.

        Returns:
            None

        Raises:
            TimeoutException: If login page does not load in time.
        """
        login_url = f"{self.base_url}/login"
        self.driver.get(login_url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.USERNAME_INPUT)
            )
        except TimeoutException:
            raise TimeoutException("Login page did not load within expected time.")

    def enter_credentials(self, username: str, password: str):
        """
        Enters the provided username and password into the login form.

        Args:
            username (str): Username to enter.
            password (str): Password to enter.

        Returns:
            None

        Raises:
            NoSuchElementException: If input fields are not found.
        """
        username_input = self.driver.find_element(*self.USERNAME_INPUT)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)

    def click_login_button(self):
        """
        Clicks the login button.

        Returns:
            None

        Raises:
            NoSuchElementException: If login button is not found.
        """
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()

    def is_login_successful(self) -> bool:
        """
        Verifies if login was successful by checking for dashboard indicator.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.DASHBOARD_INDICATOR)
            )
            return True
        except TimeoutException:
            return False

    def is_error_message_displayed(self) -> bool:
        """
        Verifies if error message is displayed after invalid login.

        Returns:
            bool: True if error message is displayed, False otherwise.
        """
        try:
            error_elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            if error_elem.is_displayed():
                return True
            return False
        except TimeoutException:
            return False
