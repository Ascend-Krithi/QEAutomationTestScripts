# LoginPage.py
"""
PageClass for Login Page
Covers: TC_LOGIN_002 (invalid credentials), TC_LOGIN_003 (empty fields), TC_Login_10 (max length validation), TC_LOGIN_004 (max length validation)
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
    - TC_LOGIN_002: Invalid credentials scenario.
    - TC_LOGIN_003: Empty fields scenario.
    - TC_Login_10: Maximum allowed length validation for email and password fields.
    - TC_LOGIN_004: Maximum allowed character input for email/username and password fields.
    Implements robust, atomic methods and comprehensive error validation.
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

    def login_with_invalid_credentials(self, email: str, password: str) -> bool:
        """
        Attempts login with invalid credentials and validates the error message.
        :param email: Invalid email or username
        :param password: Invalid password
        :return: True if correct error is shown, else False
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        # Update the expected error message as per application
        expected_error = "Invalid email or password"
        actual_error = self.get_error_message().strip()
        return actual_error == expected_error

    def login_with_empty_fields(self) -> dict:
        """
        Attempts login with both fields empty, email empty, and password empty, and returns error validation results.
        :return: Dict with keys 'both_empty', 'email_empty', 'password_empty' and boolean values for each
        """
        results = {}
        # Both fields empty
        self.enter_email("")
        self.enter_password("")
        self.click_login()
        results['both_empty'] = self.get_error_message().strip() == "Email/Username required"
        # Email empty
        self.enter_email("")
        self.enter_password("ValidPassword123")
        self.click_login()
        results['email_empty'] = self.get_error_message().strip() == "Email/Username required"
        # Password empty
        self.enter_email("valid@email.com")
        self.enter_password("")
        self.click_login()
        results['password_empty'] = self.get_error_message().strip() == "Password required"
        return results

    def validate_error_message(self, expected_message: str) -> bool:
        """
        Validates the displayed error message matches the expected message.
        :param expected_message: The expected error message text
        :return: True if matches, False otherwise
        """
        actual_message = self.get_error_message().strip()
        return actual_message == expected_message.strip()

    # --- Added for TC_Login_10 and TC_LOGIN_004 ---
    def enter_max_length_email(self, email: str) -> bool:
        """
        Enters a maximum length email/username in the email input field and verifies the input value.
        :param email: Email string at maximum allowed length (e.g., 254 chars)
        :return: True if field accepts input up to maximum length, False otherwise
        """
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        actual_value = email_input.get_attribute("value")
        return len(actual_value) == len(email)

    def enter_max_length_password(self, password: str) -> bool:
        """
        Enters a maximum length password in the password input field and verifies the input value.
        :param password: Password string at maximum allowed length (e.g., 64/128 chars)
        :return: True if field accepts input up to maximum length, False otherwise
        """
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)
        actual_value = password_input.get_attribute("value")
        return len(actual_value) == len(password)

    def login_with_max_length_credentials(self, email: str, password: str) -> dict:
        """
        Attempts login with maximum length email and password.
        :param email: Maximum length email/username
        :param password: Maximum length password
        :return: Dict with keys 'email_field', 'password_field', 'login_result', 'error_message'
        """
        email_ok = self.enter_max_length_email(email)
        password_ok = self.enter_max_length_password(password)
        self.click_login()
        # Check if login was successful or error message displayed
        error_msg = self.get_error_message().strip()
        login_success = error_msg == ""  # Assuming empty error means success
        return {
            "email_field": email_ok,
            "password_field": password_ok,
            "login_result": login_success,
            "error_message": error_msg
        }
