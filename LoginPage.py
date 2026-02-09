# LoginPage.py
"""
PageClass for Login Page
Covers: TC_Login_07 (login without 'Remember Me', session expiration after browser reopen), TC_LOGIN_001 (positive login with valid credentials, redirect to dashboard)
Strict adherence to Selenium Python best practices, atomic methods, robust locator handling, and comprehensive docstrings.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login Page.
    Covers:
    - TC_Login_07: Login without 'Remember Me', session expiration after browser reopen.
    - TC_LOGIN_001: Positive login with valid credentials, redirect to dashboard.
    """

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    REMEMBER_ME_CHECKBOX = (By.ID, "rememberMe")  # Assumed locator
    ERROR_MESSAGE = (By.ID, "errorMsg")

    def __init__(self, driver: WebDriver):
        """
        Initializes the LoginPage with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login_page(self, url: str):
        """
        Navigates to the login page.
        :param url: URL of the login page
        """
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def enter_email(self, email: str):
        """
        Enters the email/username in the email input field.
        :param email: Email or username string
        """
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        """
        Enters the password in the password input field.
        :param password: Password string
        """
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)

    def is_remember_me_selected(self) -> bool:
        """
        Checks if the 'Remember Me' checkbox is selected.
        :return: True if selected, False otherwise
        """
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))
        return checkbox.is_selected()

    def set_remember_me(self, select: bool):
        """
        Sets the 'Remember Me' checkbox to the desired state.
        :param select: True to select, False to deselect
        """
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        if checkbox.is_selected() != select:
            checkbox.click()

    def click_login(self):
        """
        Clicks the login button.
        """
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def get_error_message(self) -> str:
        """
        Returns the error message displayed on the login page.
        :return: Error message text
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return ""

    def login_with_credentials(self, email: str, password: str, remember_me: bool = False):
        """
        Enters credentials, sets 'Remember Me', and clicks login.
        :param email: Email or username
        :param password: Password
        :param remember_me: Whether to select 'Remember Me'
        """
        self.enter_email(email)
        self.enter_password(password)
        self.set_remember_me(remember_me)
        self.click_login()

    def validate_missing_email_error(self, password: str) -> bool:
        """
        Attempts login with missing email/username and validates the error message.
        :param password: Valid password
        :return: True if correct error is shown, else False
        """
        self.enter_email("")
        self.enter_password(password)
        self.click_login()
        return self.get_error_message().strip() == "Email/Username required"

    def validate_missing_password_error(self, email: str) -> bool:
        """
        Attempts login with missing password and validates the error message.
        :param email: Valid email/username
        :return: True if correct error is shown, else False
        """
        self.enter_email(email)
        self.enter_password("")
        self.click_login()
        return self.get_error_message().strip() == "Password required"
