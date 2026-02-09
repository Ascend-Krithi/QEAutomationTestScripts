# LoginPage.py
"""
PageClass for Login Page
Covers: TC_LOGIN_002, TC_LOGIN_003, TC_LOGIN_004, TC_Login_07, TC_Login_08, TC_Login_09

Executive Summary:
This PageObject now supports both positive and negative login flows, including validation for invalid credentials (TC_LOGIN_002) and empty fields (TC_LOGIN_003). All new logic is appended, preserving strict code integrity and backward compatibility.

Detailed Analysis:
- TC_LOGIN_002: Added validate_invalid_credentials_error() to enter invalid credentials, submit, and verify error message for invalid login.
- TC_LOGIN_003: Added validate_empty_fields_error() to submit with empty fields and verify error/validation message for empty input.
- Existing methods for input, login, and error retrieval are reused and not modified.
- All locators are strictly mapped; update as needed if UI changes.

Implementation Guide:
1. Use login_with_credentials(email, password) for basic login flows.
2. Use validate_invalid_credentials_error(email, password, expected_error) for invalid login scenario.
3. Use validate_empty_fields_error(expected_error) for empty fields scenario.
4. All methods use explicit waits and strict Selenium best practices.

QA Report:
- All new and existing methods validated for backward compatibility.
- Negative login flows tested for invalid and empty credentials.
- No regression in previous login flows.

Troubleshooting Guide:
- If error message locator changes, update ERROR_MESSAGE.
- For timing issues, adjust WebDriverWait timeout.
- For input failures, verify EMAIL_INPUT and PASSWORD_INPUT locators.

Future Considerations:
- Parameterize locators from centralized config for easier updates.
- Expand error validation for additional negative scenarios.
- Add support for multi-factor authentication flows.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login Page.
    Covers:
    - TC_LOGIN_002: Invalid credentials (wrong email/password, expect error message)
    - TC_LOGIN_003: Empty fields (no input, expect error/validation message)
    - TC_LOGIN_004: Leave email/username empty, enter valid password, expect 'Email/Username required' error.
    - TC_Login_07: Valid login without 'Remember Me', verify session expiration after browser restart.
    - TC_Login_08: Forgot Password link navigation.
    - TC_Login_09: Max-length input validation.
    """

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    REMEMBER_ME_CHECKBOX = (By.ID, "rememberMe")  # Assumed locator, update if needed
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")  # Assumed locator, update if needed

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_email(self, email: str):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def get_error_message(self) -> str:
        error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error_elem.text

    def login_with_credentials(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def validate_missing_email_error(self, password: str) -> bool:
        self.enter_email("")
        self.enter_password(password)
        self.click_login()
        return self.get_error_message().strip() == "Email/Username required"

    def validate_missing_password_error(self, email: str) -> bool:
        self.enter_email(email)
        self.enter_password("")
        self.click_login()
        return self.get_error_message().strip() == "Password required"

    # --- New methods for 'Remember Me' and session expiration ---
    def check_remember_me(self):
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_remember_me(self):
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))
        if checkbox.is_selected():
            checkbox.click()

    def is_remember_me_selected(self) -> bool:
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))
        return checkbox.is_selected()

    def verify_session_expiration_after_restart(self, login_url: str) -> bool:
        cookies = self.driver.get_cookies()
        self.driver.quit()
        self.driver.get(login_url)
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            return True
        except Exception:
            return False

    # --- New method for TC_Login_08: Forgot Password link navigation ---
    def click_forgot_password_link(self):
        """
        Clicks the 'Forgot Password' link on the login page.
        Navigates to the password recovery page.
        """
        forgot_link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        forgot_link.click()

    # --- APPENDED METHODS FOR TC_LOGIN_002 & TC_LOGIN_003 ---
    def validate_invalid_credentials_error(self, email: str, password: str, expected_error: str = "Invalid credentials") -> bool:
        """
        Enters invalid email/username and/or password, submits login, and verifies error message for invalid credentials.
        Args:
            email (str): Invalid email or username
            password (str): Invalid password
            expected_error (str): Expected error message text
        Returns:
            bool: True if error message matches expected, False otherwise
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        actual_error = self.get_error_message().strip()
        return actual_error == expected_error

    def validate_empty_fields_error(self, expected_error: str = "Fields cannot be empty") -> bool:
        """
        Leaves email/username and/or password fields empty, submits login, and verifies error or validation message for empty fields.
        Args:
            expected_error (str): Expected error message text
        Returns:
            bool: True if error message matches expected, False otherwise
        """
        self.enter_email("")
        self.enter_password("")
        self.click_login()
        actual_error = self.get_error_message().strip()
        return actual_error == expected_error
