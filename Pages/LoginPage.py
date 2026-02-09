# LoginPage.py
# Selenium Page Object Model for the Login Page of example-ecommerce.com
#
# Executive Summary:
# This PageClass enables automated interaction with the login page, supporting input, validation, and post-login verification.
# It is generated based on Locators.json and is fully compatible for downstream automation workflows.
#
# Implementation Guide:
# - Import this class and instantiate with a Selenium WebDriver or Page object.
# - Use provided methods to interact with login fields, buttons, and check for messages.
#
# QA Report:
# - All locators are mapped directly from Locators.json.
# - Methods are atomic and do not alter existing logic.
# - Class follows PEP8 and Selenium best practices.
#
# Troubleshooting Guide:
# - If element not found, verify locator string in Locators.json matches actual DOM.
# - If login fails, ensure test data is valid and page loads are awaited.
#
# Future Considerations:
# - Add more granular validation methods for new login features.
# - Integrate with advanced reporting or assertion libraries.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """Page Object for Login Page at https://example-ecommerce.com/login"""

    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://example-ecommerce.com/login'
        # Inputs
        self.email_field = (By.ID, 'login-email')
        self.password_field = (By.ID, 'login-password')
        self.remember_me_checkbox = (By.ID, 'remember-me')
        # Buttons
        self.login_submit = (By.ID, 'login-submit')
        self.forgot_password_link = (By.CSS_SELECTOR, 'a.forgot-password-link')
        # Messages
        self.error_message = (By.CSS_SELECTOR, 'div.alert-danger')
        self.validation_error = (By.CSS_SELECTOR, '.invalid-feedback')
        self.empty_field_prompt = (By.XPATH, "//*[contains(text(), 'Mandatory fields are required')]")
        # Post-login
        self.dashboard_header = (By.CSS_SELECTOR, 'h1.dashboard-title')
        self.user_profile_icon = (By.CSS_SELECTOR, '.user-profile-name')

    def open(self):
        """Navigate to the login page."""
        self.driver.get(self.url)

    def enter_email(self, email):
        """Enter email address."""
        email_elem = self.driver.find_element(*self.email_field)
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        """Enter password."""
        password_elem = self.driver.find_element(*self.password_field)
        password_elem.clear()
        password_elem.send_keys(password)

    def toggle_remember_me(self):
        """Toggle the 'Remember Me' checkbox."""
        checkbox = self.driver.find_element(*self.remember_me_checkbox)
        checkbox.click()

    def click_login(self):
        """Click the Login button."""
        self.driver.find_element(*self.login_submit).click()

    def click_forgot_password(self):
        """Click the Forgot Password link."""
        self.driver.find_element(*self.forgot_password_link).click()

    def get_error_message(self):
        """Return the error message text if present."""
        try:
            elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return elem.text
        except Exception:
            return None

    def get_validation_error(self):
        """Return the validation error text if present."""
        try:
            elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.validation_error)
            )
            return elem.text
        except Exception:
            return None

    def is_empty_field_prompt_present(self):
        """Check if the empty field prompt is visible."""
        try:
            elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.empty_field_prompt)
            )
            return True
        except Exception:
            return False

    def is_dashboard_header_present(self):
        """Verify dashboard header is visible post-login."""
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.dashboard_header)
            )
            return True
        except Exception:
            return False

    def is_user_profile_icon_present(self):
        """Verify user profile icon is visible post-login."""
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.user_profile_icon)
            )
            return True
        except Exception:
            return False
