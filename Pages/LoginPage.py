# LoginPage.py
"""
PageClass for Login Page
Covers: TC_LOGIN_003 (leave email/username empty), TC_LOGIN_004 (leave password empty)
Ensures negative login error handling for missing credentials.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login Page.
    Covers negative scenarios:
    - TC_LOGIN_003: Leave email/username empty, enter valid password, expect 'Email/Username required' error.
    - TC_LOGIN_004: Enter valid email/username, leave password empty, expect 'Password required' error.
    """

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")

    def __init__(self, driver: WebDriver):
        """
        Initializes the LoginPage with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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
        error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error_elem.text

    def login_with_credentials(self, email: str, password: str):
        """
        Enters credentials and clicks login.
        :param email: Email or username
        :param password: Password
        """
        self.enter_email(email)
        self.enter_password(password)
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
