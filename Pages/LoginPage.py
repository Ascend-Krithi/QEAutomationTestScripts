from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_URL = "https://your-app-domain.com/login"
    EMAIL_INPUT = (By.ID, "email-input")
    USERNAME_INPUT = (By.ID, "username-input")
    PASSWORD_INPUT = (By.ID, "password-input")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.ID, "login-error")
    CAPTCHA_ELEMENT = (By.ID, "captcha")
    LOCKOUT_MESSAGE = (By.ID, "lockout-msg")
    RATE_LIMIT_MESSAGE = (By.ID, "rate-limit-msg")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self):
        self.driver.get(self.LOGIN_URL)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON))

    def enter_credentials(self, email_or_username: str, password: str):
        try:
            email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            email_input.clear()
            email_input.send_keys(email_or_username)
        except Exception:
            username_input = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
            username_input.clear()
            username_input.send_keys(email_or_username)
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return None

    def is_captcha_present(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.CAPTCHA_ELEMENT))
            return True
        except Exception:
            return False

    def is_lockout_message_present(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOCKOUT_MESSAGE))
            return True
        except Exception:
            return False

    def is_rate_limit_message_present(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.RATE_LIMIT_MESSAGE))
            return True
        except Exception:
            return False

    def rapid_invalid_login_attempts(self, email_or_username: str, password: str, attempts: int = 10):
        self.navigate_to_login()
        for _ in range(attempts):
            self.enter_credentials(email_or_username, password)
            self.click_login()
        # Check for lockout, rate limit, or captcha
        if self.is_captcha_present():
            return "Captcha triggered after rapid attempts."
        elif self.is_lockout_message_present():
            return "Lockout message triggered after rapid attempts."
        elif self.is_rate_limit_message_present():
            return "Rate limiting message triggered after rapid attempts."
        else:
            return "No security mechanism detected after rapid invalid login attempts."

    def login_with_case_variations(self, email_or_username: str, password: str):
        self.navigate_to_login()
        self.enter_credentials(email_or_username, password)
        self.click_login()
        error_message = self.get_error_message()
        if error_message:
            return f"Login failed: {error_message}"
        else:
            return "Login succeeded."
