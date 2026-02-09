# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    EMAIL_MAX_LENGTH = 254
    PASSWORD_MAX_LENGTH = 128

    # Locators from Locators.json
    EMAIL_INPUT = (By.ID, 'email-field')  # Update according to actual locator
    PASSWORD_INPUT = (By.ID, 'password-field')  # Update according to actual locator
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-testid='login-btn']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login_page(self, url):
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def enter_email(self, email):
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(email[:self.EMAIL_MAX_LENGTH])

    def enter_password(self, password):
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password[:self.PASSWORD_MAX_LENGTH])

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def is_login_successful(self):
        # Implementation depends on post-login landing, e.g., DashboardPage element presence
        try:
            self.wait.until(EC.url_changes(self.driver.current_url))
            return True
        except:
            return False

    def get_error_message(self):
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except:
            return None

    def login_with_credentials(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        if self.is_login_successful():
            return "Login successful"
        else:
            return self.get_error_message()
