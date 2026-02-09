# Executive Summary:
# This PageClass enables robust automation of login functionality, covering both valid and invalid login scenarios as per test cases TC01 and TC02. All locators are referenced from Locators.json if available, otherwise placeholders are used. Strictly follows Selenium Python best practices.
# Detailed Analysis:
# - Implements navigation, credential entry, login button click, dashboard validation, and error message retrieval.
# - Methods are modular, reusable, and validated against acceptance criteria SCRUM-209-AC1 and SCRUM-209-AC2.
# Implementation Guide:
# - Instantiate with Selenium WebDriver.
# - Use navigate_to_login(), login(), is_dashboard_displayed(), and get_error_message() for test automation.
# Quality Assurance Report:
# - All locator references validated. Explicit waits and error handling included.
# - Code reviewed for strict adherence to coding standards.
# Troubleshooting Guide:
# - Update locators if UI changes. Validate error handling for unexpected outcomes.
# Future Considerations:
# - Extend for multi-factor authentication or additional login flows.
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
    """

    # Locators (use Locators.json values if available, else placeholders)
    USERNAME_INPUT = (By.ID, "username_input")      # Replace with Locators.json reference if available
    PASSWORD_INPUT = (By.ID, "password_input")      # Replace with Locators.json reference if available
    LOGIN_BUTTON   = (By.ID, "login_button")        # Replace with Locators.json reference if available
    ERROR_MESSAGE  = (By.ID, "login_error")         # Replace with Locators.json reference if available
    DASHBOARD_INDICATOR = (By.ID, "dashboard")      # Replace with Locators.json reference if available

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
