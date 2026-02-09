import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://example-ecommerce.com/login"
        self.email_field = (By.ID, "login-email")
        self.password_field = (By.ID, "login-password")
        self.remember_me_checkbox = (By.ID, "remember-me")
        self.login_submit = (By.ID, "login-submit")
        self.forgot_password_link = (By.CSS_SELECTOR, "a.forgot-password-link")
        self.error_message = (By.CSS_SELECTOR, "div.alert-danger")
        self.validation_error = (By.CSS_SELECTOR, ".invalid-feedback")
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
        self.user_profile_icon = (By.CSS_SELECTOR, ".user-profile-name")

    def open(self):
        self.driver.get(self.url)

    def enter_email(self, email):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.email_field)).clear()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.email_field)).send_keys(email)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.password_field)).clear()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.password_field)).send_keys(password)

    def click_remember_me(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.remember_me_checkbox)).click()

    def click_login(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_submit)).click()

    def click_forgot_password(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.forgot_password_link)).click()

    def get_error_message(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.error_message)).text
        except:
            return None

    def get_validation_error(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.validation_error)).text
        except:
            return None

    def get_empty_field_prompt(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.empty_field_prompt)).text
        except:
            return None

    def is_dashboard_header_visible(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.dashboard_header))
            return True
        except:
            return False

    def is_user_profile_icon_visible(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.user_profile_icon))
            return True
        except:
            return False
