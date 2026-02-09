# Executive Summary
# This PageClass was generated based on test cases TC-FT-001 and TC-FT-002, and Locators.json data for LoginPage.
# It encapsulates all necessary elements and actions for login-related automation in the AXOS project.

# Detailed Analysis
# The LoginPage class provides methods for interacting with login form elements, submitting credentials, handling error messages, and verifying post-login states.
# All locators are sourced from Locators.json, ensuring consistent mapping between UI and automation.

# Implementation Guide
# Usage Example:
# from Pages.LoginPage import LoginPage
# login_page = LoginPage(driver)
# login_page.open()
# login_page.enter_email('user@example.com')
# login_page.enter_password('securepassword')
# login_page.toggle_remember_me(True)
# login_page.submit_login()
# assert login_page.is_dashboard_visible()

# Quality Assurance Report
# - All methods are atomic and do not alter existing logic.
# - Locators are strictly mapped from Locators.json.
# - Code is validated for syntax, structure, and downstream compatibility.
# - No existing PageClasses are overwritten.

# Troubleshooting Guide
# - If an element is not found, verify Locators.json matches current UI.
# - Ensure Selenium WebDriver is properly initialized and passed to the PageClass.
# - Use explicit waits for dynamic elements if needed.

# Future Considerations
# - Extend with additional post-login validations as new features are released.
# - Refactor to support multi-factor authentication if required.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    def __init__(self, driver):
        self.driver = driver
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
        self.driver.get(self.URL)

    def enter_email(self, email):
        email_elem = self.driver.find_element(*self.email_field)
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        password_elem = self.driver.find_element(*self.password_field)
        password_elem.clear()
        password_elem.send_keys(password)

    def toggle_remember_me(self, enable=True):
        checkbox = self.driver.find_element(*self.remember_me_checkbox)
        if checkbox.is_selected() != enable:
            checkbox.click()

    def submit_login(self):
        self.driver.find_element(*self.login_submit).click()

    def click_forgot_password(self):
        self.driver.find_element(*self.forgot_password_link).click()

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_message).text
        except:
            return None

    def get_validation_error(self):
        try:
            return self.driver.find_element(*self.validation_error).text
        except:
            return None

    def is_empty_field_prompt_visible(self):
        try:
            return self.driver.find_element(*self.empty_field_prompt).is_displayed()
        except:
            return False

    def is_dashboard_visible(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.dashboard_header)
            )
            return True
        except:
            return False

    def is_user_profile_icon_visible(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.user_profile_icon)
            )
            return True
        except:
            return False
