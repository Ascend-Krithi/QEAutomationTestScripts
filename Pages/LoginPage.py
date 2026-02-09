from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for Login functionality.
    Locators and flows based on Locators.json.
    """
    URL = 'https://example-ecommerce.com/login'

    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.ID, 'login-email')
        self.password_field = (By.ID, 'login-password')
        self.remember_me_checkbox = (By.ID, 'remember-me')
        self.login_submit = (By.ID, 'login-submit')
        self.forgot_password_link = (By.CSS_SELECTOR, 'a.forgot-password-link')
        self.error_message = (By.CSS_SELECTOR, 'div.alert-danger')
        self.validation_error = (By.CSS_SELECTOR, '.invalid-feedback')
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, 'h1.dashboard-title')
        self.user_profile_icon = (By.CSS_SELECTOR, '.user-profile-name')

    def load(self):
        self.driver.get(self.URL)

    def login(self, email, password, remember_me=False):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.email_field)).send_keys(email)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.password_field)).send_keys(password)
        if remember_me:
            checkbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.remember_me_checkbox))
            if not checkbox.is_selected():
                checkbox.click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_submit)).click()

    def get_error_message(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.error_message)).text
        except:
            return None

    def is_dashboard_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.dashboard_header))
            return True
        except:
            return False

    def click_forgot_password(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.forgot_password_link)).click()
