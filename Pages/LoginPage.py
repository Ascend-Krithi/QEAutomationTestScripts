from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    # Locators
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def enter_email(self, email: str):
        self.driver.find_element(*self.EMAIL_FIELD).clear()
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)

    def enter_password(self, password: str):
        self.driver.find_element(*self.PASSWORD_FIELD).clear()
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def toggle_remember_me(self):
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        checkbox.click()

    def click_login(self):
        self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON).click()

    def click_forgot_password(self):
        self.driver.find_element(*self.FORGOT_PASSWORD_LINK).click()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def get_validation_error(self):
        return self.driver.find_element(*self.VALIDATION_ERROR).text

    def is_empty_field_prompt_visible(self):
        try:
            self.driver.find_element(*self.EMPTY_FIELD_PROMPT)
            return True
        except:
            return False

    def is_dashboard_header_visible(self):
        try:
            self.driver.find_element(*self.DASHBOARD_HEADER)
            return True
        except:
            return False

    def is_user_profile_icon_visible(self):
        try:
            self.driver.find_element(*self.USER_PROFILE_ICON)
            return True
        except:
            return False
