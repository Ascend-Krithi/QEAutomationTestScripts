from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_login_page(self):
        self.driver.get(self.URL)

    def enter_email(self, email: str):
        self.driver.find_element(*self.EMAIL_FIELD).clear()
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)

    def enter_password(self, password: str):
        self.driver.find_element(*self.PASSWORD_FIELD).clear()
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def click_remember_me(self):
        self.driver.find_element(*self.REMEMBER_ME_CHECKBOX).click()

    def submit_login(self):
        self.driver.find_element(*self.LOGIN_SUBMIT).click()

    def click_forgot_password(self):
        self.driver.find_element(*self.FORGOT_PASSWORD_LINK).click()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def get_validation_error(self):
        return self.driver.find_element(*self.VALIDATION_ERROR).text

    def get_empty_field_prompt(self):
        return self.driver.find_element(*self.EMPTY_FIELD_PROMPT).text

    def is_logged_in(self):
        return self.driver.find_element(*self.DASHBOARD_HEADER).is_displayed()

    def get_user_profile_name(self):
        return self.driver.find_element(*self.USER_PROFILE_ICON).text
