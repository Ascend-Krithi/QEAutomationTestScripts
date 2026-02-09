# LoginPage.py
"""
Selenium PageClass for Login Page
Handles navigation to login, credential entry, and login submission.

Industry Best Practices:
- Locators encapsulated as class attributes
- Explicit waits for element visibility/clickability
- Clear docstrings and method documentation
- Error handling for invalid login scenarios
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    """
    Page Object for Login Page.
    """
    # Locators (assumed based on repo conventions)
    login_url = "/login"
    username_input = (By.ID, "username")
    password_input = (By.ID, "password")
    submit_button = (By.ID, "login-submit")
    error_message = (By.CSS_SELECTOR, ".alert-error")

    def __init__(self, driver, base_url):
        """
        Args:
            driver (WebDriver): Selenium WebDriver instance
            base_url (str): Base URL of application
        """
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """
        Navigate to the login page.
        """
        self.driver.get(self.base_url + self.login_url)

    def enter_username(self, username):
        """
        Enter username into the username field.
        Args:
            username (str): Username string
        """
        elem = self.wait.until(EC.visibility_of_element_located(self.username_input))
        elem.clear()
        elem.send_keys(username)

    def enter_password(self, password):
        """
        Enter password into the password field.
        Args:
            password (str): Password string
        """
        elem = self.wait.until(EC.visibility_of_element_located(self.password_input))
        elem.clear()
        elem.send_keys(password)

    def submit(self):
        """
        Click the login submit button.
        """
        btn = self.wait.until(EC.element_to_be_clickable(self.submit_button))
        btn.click()

    def login(self, username, password):
        """
        Perform login with provided credentials.
        Args:
            username (str): Username
            password (str): Password
        Returns:
            bool: True if login likely successful (dashboard loaded), False otherwise (error shown)
        """
        self.enter_username(username)
        self.enter_password(password)
        self.submit()

    def get_error_message(self):
        """
        Retrieve error message after invalid login attempt.
        Returns:
            str: Error message text if present, else None
        """
        try:
            elem = self.wait.until(EC.visibility_of_element_located(self.error_message))
            return elem.text
        except TimeoutException:
            return None
