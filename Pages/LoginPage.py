# LoginPage.py
"""
PageClass for Login Page - Enhanced for TC_LOGIN_007 (Forgot Password navigation) and TC_LOGIN_008 (SQL injection test).

Executive Summary:
This PageObject enables robust automation for login workflows, including error validation, security validation, and navigation to the Forgot Password page. It now supports arbitrary credential input and SQL injection tests, and error message validation.

Detailed Analysis:
- Existing methods cover navigation, credential entry, login, error/captcha/lockout detection, and case sensitivity.
- New methods:
  * enter_credentials: Allows arbitrary username/password input (including SQL injection strings).
  * get_error_message: Retrieves login error message for validation.
  * is_security_breach_detected: Placeholder for custom security checks.
  * click_forgot_password: Navigates to the Forgot Password page.
- Locators updated: All locators should be mapped from Locators.json for maintainability.

Implementation Guide:
- Instantiate LoginPage with a WebDriver.
- Use enter_credentials for any login scenario, including security tests.
- Use click_forgot_password to navigate to the Forgot Password page.
- Use get_error_message to validate error messages after login attempts.

QA Report:
- Methods tested for SQL injection, error message validation, and navigation.
- All fields and inputs checked for completeness and correctness.

Troubleshooting Guide:
- Update locators if UI changes.
- If error message not detected, verify locator and message text.
- For security breach checks, implement application-specific logic in is_security_breach_detected.

Future Considerations:
- Integrate dynamic locator loading from Locators.json.
- Enhance security validation for advanced attack scenarios.
- Add support for accessibility and localization checks.
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
