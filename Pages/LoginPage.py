"""
LoginPage PageClass for Selenium-based automation.

Implements methods to:
- Navigate to the login page
- Enter username and password
- Click the login button
- Verify login success (redirect to dashboard/home)
- Verify error messages for invalid login

Locators are defined as placeholders and should be updated to match the application's actual elements.
Strictly follows best practices and integrates with existing PageClasses (ProfilePage, RuleConfigurationPage, SettingsPage).

Author: [Your Name]
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # Placeholder locators. Update these as per Locators.json or actual application.
    USERNAME_INPUT = (By.ID, "login-username")         # e.g., id="login-username"
    PASSWORD_INPUT = (By.ID, "login-password")         # e.g., id="login-password"
    LOGIN_BUTTON = (By.ID, "login-button")             # e.g., id="login-button"
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".login-error")  # e.g., css=".login-error"
    DASHBOARD_INDICATOR = (By.ID, "dashboard-home")    # e.g., id="dashboard-home"

    LOGIN_URL = "/login"  # Update with actual login page URL path

    def __init__(self, driver, base_url):
        """
        :param driver: Selenium WebDriver instance
        :param base_url: Base URL of the application
        """
        self.driver = driver
        self.base_url = base_url

    def go_to_login_page(self):
        """
        Navigates to the login page.
        """
        self.driver.get(f"{self.base_url}{self.LOGIN_URL}")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )

    def enter_username(self, username):
        """
        Enters the username into the username input field.
        """
        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        """
        Enters the password into the password input field.
        """
        password_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """
        Clicks the login button.
        """
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_btn.click()

    def is_login_successful(self):
        """
        Verifies if login was successful by checking for dashboard/home page indicator.
        :return: True if dashboard/home is displayed, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.DASHBOARD_INDICATOR)
            )
            return True
        except:
            return False

    def is_error_message_displayed(self, expected_message="Invalid username or password"):
        """
        Verifies if the error message for invalid login is displayed.
        :param expected_message: Expected error message text.
        :return: True if error message is displayed and matches expected text, False otherwise.
        """
        try:
            error_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return expected_message in error_elem.text
        except:
            return False

    def login(self, username, password):
        """
        Performs the complete login process and returns success status.
        :param username: Username to enter
        :param password: Password to enter
        :return: True if login successful, False otherwise
        """
        self.go_to_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self.is_login_successful()

    def login_with_invalid_credentials(self, username, password):
        """
        Attempts login with invalid credentials and checks for error message.
        :param username: Username to enter
        :param password: Password to enter
        :return: True if error message is displayed, False otherwise
        """
        self.go_to_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self.is_error_message_displayed()

# Usage Example (for test scripts):
# from LoginPage import LoginPage
# login_page = LoginPage(driver, base_url)
# login_page.login("valid_user", "ValidPass123")
# assert login_page.is_login_successful()
# login_page.login_with_invalid_credentials("invalid_user", "WrongPass")
# assert login_page.is_error_message_displayed()
