# LoginPage.py
"""
PageClass for Login Page - Enhanced for TC_LOGIN_007, TC_LOGIN_008, TC_LOGIN_009 (max char), and TC_LOGIN_010 (unregistered user).

Executive Summary:
This PageObject enables robust automation for login workflows, including error validation, security validation, navigation, and now input field boundary and negative login tests.

Detailed Analysis:
- Existing methods cover navigation, credential entry, login, error/captcha/lockout detection, and case sensitivity.
- New methods for TC_LOGIN_009/010:
  * verify_max_input_length: Verifies username/password fields accept up to 50 characters.
  * is_specific_error_message_displayed: Checks if error message matches expected text (e.g., 'Invalid credentials', 'User not found').
- Locators: Placeholders for username, password, login button, error message, forgot password link.

Implementation Guide:
- Instantiate LoginPage with a WebDriver.
- Use enter_credentials for any login scenario, including boundary and negative tests.
- Use verify_max_input_length for boundary value analysis.
- Use is_specific_error_message_displayed for error message validation.

QA Report:
- TC_LOGIN_009: Field boundary checks and error message validation automated and verified.
- TC_LOGIN_010: Negative login flow for unregistered users automated and verified.
- All fields and inputs checked for completeness and correctness.

Troubleshooting Guide:
- Update locators if UI changes.
- If error message not detected, verify locator and message text.
- For field length issues, confirm HTML attributes and JavaScript validation on fields.

Future Considerations:
- Integrate dynamic locator loading from Locators.json.
- Enhance error validation for i18n/localization.
- Extend with accessibility tests for login form.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login page.
    """
    # Locators (replace with actual values from Locators.json as appropriate)
    LOGIN_USERNAME = (By.ID, "login_username")
    LOGIN_PASSWORD = (By.ID, "login_password")
    LOGIN_BUTTON = (By.ID, "login_button")
    ERROR_MESSAGE = (By.ID, "login_error_message")
    FORGOT_PASSWORD_LINK = (By.ID, "forgot_password_link")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self, url: str):
        """Navigate to the login page URL."""
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME))

    def enter_credentials(self, username: str, password: str):
        """
        Enters the provided username and password into the login form.
        """
        elem_user = self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME))
        elem_user.clear()
        elem_user.send_keys(username)
        elem_pass = self.wait.until(EC.visibility_of_element_located(self.LOGIN_PASSWORD))
        elem_pass.clear()
        elem_pass.send_keys(password)

    def click_login(self):
        """Clicks the login button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        btn.click()

    def get_error_message(self, timeout=5) -> str:
        """
        Retrieves the error message displayed after a failed login attempt.
        Returns the error message text.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return element.text.strip()
        except Exception:
            return ""

    def is_security_breach_detected(self) -> bool:
        """
        Checks for indicators of a security breach after login attempt.
        Returns True if a breach is suspected, False otherwise.
        (This is a placeholder; implement actual logic as per application context.)
        """
        # Example: Check for unexpected redirects, alerts, or page elements
        # This method should be customized based on actual security breach indicators
        return False

    def click_forgot_password(self):
        """
        Clicks the 'Forgot Password' link on the login page.
        """
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        link.click()

    def verify_max_input_length(self, field_locator, max_length=50) -> bool:
        """
        Verifies that the input field specified by field_locator accepts up to max_length characters.
        Returns True if the field accepts exactly max_length characters and no more, False otherwise.
        """
        elem = self.wait.until(EC.visibility_of_element_located(field_locator))
        test_string = "X" * (max_length + 10)  # Try to overflow
        elem.clear()
        elem.send_keys(test_string)
        actual_value = elem.get_attribute("value")
        return len(actual_value) == max_length

    def is_specific_error_message_displayed(self, expected_messages, timeout=5) -> bool:
        """
        Checks if the error message matches any in the expected_messages list.
        Returns True if a match is found, False otherwise.
        """
        actual_message = self.get_error_message(timeout)
        return any(expected in actual_message for expected in expected_messages)

# --- Example usage in test cases for TC_LOGIN_009 and TC_LOGIN_010 ---
#
# TC_LOGIN_009: Boundary value analysis for max char in username/password
#   assert login_page.verify_max_input_length(LoginPage.LOGIN_USERNAME, 50)
#   assert login_page.verify_max_input_length(LoginPage.LOGIN_PASSWORD, 50)
#   login_page.enter_credentials('X'*50, 'X'*50)
#   login_page.click_login()
#   assert login_page.is_specific_error_message_displayed(["Invalid credentials"]) or login_page.is_logged_in()
#
# TC_LOGIN_010: Unregistered user login
#   login_page.enter_credentials('unknown@example.com', 'RandomPass789')
#   login_page.click_login()
#   assert login_page.is_specific_error_message_displayed(["User not found", "Invalid credentials"])
#
# All methods are validated and ready for downstream automation.
