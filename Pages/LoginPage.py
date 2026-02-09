from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_URL = "https://your-app-domain.com/login"  # Replace with actual login URL

    # Locators (generic, update as needed)
    EMAIL_INPUT = (By.ID, "email-input")  # Replace with actual locator
    USERNAME_INPUT = (By.ID, "username-input")  # Replace with actual locator
    PASSWORD_INPUT = (By.ID, "password-input")  # Replace with actual locator
    LOGIN_BUTTON = (By.ID, "login-button")  # Replace with actual locator
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")  # Replace with actual locator
    ERROR_MESSAGE = (By.ID, "login-error")  # Replace with actual locator for error message
    VALIDATION_MESSAGE = (By.ID, "login-validation")  # Replace with actual locator for empty field validation

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self):
        self.driver.get(self.LOGIN_URL)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON))

    def click_forgot_password(self):
        forgot_password = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        forgot_password.click()

    def enter_max_length_email_and_valid_password(self, email: str, password: str):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)

    def enter_max_length_username_and_valid_password(self, username: str, password: str):
        username_input = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        username_input.clear()
        username_input.send_keys(username)
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    # --- New Functions for Negative Scenarios ---
    def enter_invalid_credentials(self, email_or_username: str, password: str):
        """
        Enter invalid email/username and password for negative login test.
        """
        try:
            # Try email input first
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            email_input.clear()
            email_input.send_keys(email_or_username)
        except Exception:
            # Fallback to username input
            username_input = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
            username_input.clear()
            username_input.send_keys(email_or_username)
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)

    def leave_fields_empty(self):
        """
        Leave email/username and password fields empty for negative login test.
        """
        try:
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            email_input.clear()
        except Exception:
            pass  # If email input not present
        try:
            username_input = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
            username_input.clear()
        except Exception:
            pass  # If username input not present
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()

    def get_error_message(self):
        """
        Retrieve error message displayed for invalid credentials.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def get_validation_message(self):
        """
        Retrieve validation message displayed for empty fields.
        """
        try:
            validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_MESSAGE))
            return validation_elem.text
        except Exception:
            return None
