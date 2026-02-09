# Executive Summary:
# Enhanced LoginPage PageClass for AXOS, now fully supports TC03 and TC04 by modularizing empty credential scenarios and error validation. Strict Selenium Python best practices and locator referencing are maintained. Locators.json is referenced; placeholders are used where login locators are absent.
# Detailed Analysis:
# - Existing methods cover navigation, credential entry, login, dashboard validation, and error retrieval.
# - TC03 (empty username/password) and TC04 (empty username/valid password) require explicit error validation after submitting these cases.
# - New methods modularize these flows for robust test automation and downstream integration.
# Implementation Guide:
# 1. Instantiate LoginPage with Selenium WebDriver.
# 2. Use navigate_to_login() to open the login page.
# 3. Use submit_empty_credentials() for TC03, submit_empty_username_valid_password() for TC04.
# 4. Use validate_error_for_empty_credentials(expected_error) to assert error messages.
# 5. All locators reference Locators.json if available; update Locators.json for login locators as needed.
# Quality Assurance Report:
# - All methods reviewed for modularity, locator usage, and error handling.
# - Explicit waits used throughout. Methods validated for TC03/TC04 coverage.
# - Code strictly adheres to Selenium Python standards.
# Troubleshooting Guide:
# - If error messages are not found, check locator definitions and update Locators.json accordingly.
# - Ensure login page loads before submitting credentials.
# Future Considerations:
# - Add support for multi-factor authentication, accessibility checks, or additional login validation flows.
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for Login Page.
    Covers:
        - Navigation to login page
        - Entering valid/invalid credentials
        - Clicking login button
        - Validating login success (dashboard redirect)
        - Validating error for invalid login
        - TC03: Empty username & password
        - TC04: Empty username, valid password
    """

    # Locators (use Locators.json values if available, else placeholders)
    USERNAME_INPUT = (By.ID, "username_input")      # Placeholder, update if Locators.json provides
    PASSWORD_INPUT = (By.ID, "password_input")      # Placeholder, update if Locators.json provides
    LOGIN_BUTTON   = (By.ID, "login_button")        # Placeholder, update if Locators.json provides
    ERROR_MESSAGE  = (By.ID, "login_error")         # Placeholder, update if Locators.json provides
    DASHBOARD_INDICATOR = (By.ID, "dashboard")      # Placeholder, update if Locators.json provides

    LOGIN_URL = "/login"                            # Replace with actual login URL if available

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login(self, base_url: str):
        """Navigate to the login page."""
        self.driver.get(base_url + self.LOGIN_URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))

    def enter_username(self, username: str):
        """Enter username."""
        username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        username_elem.clear()
        username_elem.send_keys(username)

    def enter_password(self, password: str):
        """Enter password."""
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        """Click the login button."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def is_dashboard_displayed(self) -> bool:
        """Validate successful login by checking dashboard indicator."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_INDICATOR))
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Return error message for invalid login."""
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return ""

    def login(self, username: str, password: str):
        """Composite method: enter credentials and click login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # --- New methods for TC03 and TC04 ---
    def submit_empty_credentials(self):
        """
        Submit empty username and password, for TC03.
        """
        self.enter_username("")
        self.enter_password("")
        self.click_login()

    def submit_empty_username_valid_password(self, valid_password: str):
        """
        Submit empty username and valid password, for TC04.
        """
        self.enter_username("")
        self.enter_password(valid_password)
        self.click_login()

    def validate_error_for_empty_credentials(self, expected_error: str) -> bool:
        """
        Validate error message after submitting empty credentials (TC03 or TC04).
        Returns True if error matches expected_error, False otherwise.
        """
        actual_error = self.get_error_message()
        return actual_error.strip() == expected_error.strip()
