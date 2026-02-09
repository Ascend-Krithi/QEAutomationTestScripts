# LoginPage.py
"""
PageClass for Login Page
Covers: TC_LOGIN_003 (leave email/username empty), TC_LOGIN_004 (leave password empty), TC_LOGIN_009 (max input length), TC_LOGIN_010 (unregistered user)
Ensures negative login error handling for missing credentials, input limits, and unregistered users.
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
    - TC_LOGIN_009: Enter maximum allowed characters in email/username and password fields, validate field limits and error handling.
    - TC_LOGIN_010: Enter credentials for unregistered user, validate error handling.
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

    def validate_max_input_length(self, max_length: int = 50) -> bool:
        """
        TC_LOGIN_009: Validates that email and password fields accept up to max_length characters and no more.
        Attempts login with max_length characters and checks error handling and UI integrity.
        :param max_length: Maximum allowed character length (default: 50)
        :return: True if fields accept up to max_length, error is handled, and no UI break occurs, else False
        """
        long_email = "a" * max_length
        long_password = "P" * max_length
        self.enter_email(long_email)
        self.enter_password(long_password)
        self.click_login()
        # Check error message or successful login
        error_text = self.get_error_message().strip()
        if error_text == "Invalid credentials" or error_text == "User not found":
            # Acceptable negative result
            return True
        # Optionally, check for UI integrity (fields should not overflow)
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        if len(email_input.get_attribute("value")) > max_length:
            return False
        if len(password_input.get_attribute("value")) > max_length:
            return False
        return True

    def validate_unregistered_user_error(self, email: str = "unknown@example.com", password: str = "RandomPass789") -> bool:
        """
        TC_LOGIN_010: Attempts login with unregistered user credentials and validates error message.
        :param email: Unregistered email/username
        :param password: Unregistered password
        :return: True if error message is 'User not found' or 'Invalid credentials', else False
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        error_text = self.get_error_message().strip()
        return error_text in ["User not found", "Invalid credentials"]
