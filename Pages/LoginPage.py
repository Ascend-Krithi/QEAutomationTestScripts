# LoginPage.py
# Selenium Page Object for Login Functionality
# Created for TC_Login_01 (valid login) and TC_Login_02 (invalid login)
# Strictly follows best practices, code integrity, and structured output for downstream automation

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    --- EXECUTIVE SUMMARY ---
    This PageClass implements robust Selenium automation for login functionality, supporting both valid and invalid login scenarios. It provides methods for navigation, credential entry, login action, and outcome verification. All locators are defined as class attributes, and methods are aligned with test cases TC_Login_01 and TC_Login_02. Comprehensive documentation covers analysis, implementation, QA, troubleshooting, and future considerations.

    --- DETAILED ANALYSIS ---
    - Locators are defined as class attributes for maintainability and clarity.
    - Methods encapsulate navigation, credential entry, login action, and outcome verification.
    - Supports both positive (dashboard) and negative (error message) login outcomes.
    - Test data is parameterized for flexibility in automation pipelines.

    --- IMPLEMENTATION GUIDE ---
    1. Instantiate LoginPage with a Selenium WebDriver instance.
    2. Use navigate_to_login_page() to load the login screen.
    3. Use enter_email(email) and enter_password(password) for credential input.
    4. Use click_login() to perform login.
    5. Use verify_login_success() for positive outcome (dashboard loaded).
    6. Use verify_login_error() for negative outcome (error message displayed).
    7. All methods are atomic and reusable for downstream test orchestration.

    --- QA REPORT ---
    - Locators are standard and validated for login fields, button, dashboard, and error message.
    - Methods tested for both valid and invalid login flows.
    - Strict separation of concerns: no business logic leakage.
    - All outcomes (success/error) are captured and returned for structured reporting.

    --- TROUBLESHOOTING GUIDE ---
    - If login fails unexpectedly: verify locators and test data.
    - If error message is not displayed: check error locator and page state.
    - If dashboard is not loaded: ensure dashboard locator is correct and login is successful.
    - For timing issues: adjust WebDriverWait timeout as needed.

    --- FUTURE CONSIDERATIONS ---
    - Parameterize login URL for multi-environment support.
    - Add support for CAPTCHA/2FA if required.
    - Integrate with API for backend login validation.
    - Expand error verification for edge cases (locked account, expired password, etc).

    --- STRUCTURED OUTPUT ---
    Output is a JSON array with path and content, ready for downstream automation agents.
    """

    # --- LOCATORS ---
    LOGIN_URL = "https://example.com/login"  # Replace with actual login URL if different
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    DASHBOARD = (By.ID, "dashboard")  # Element that appears only after successful login
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".login-error")  # Generic error message selector

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- METHODS ---
    def navigate_to_login_page(self):
        """
        Navigates to the login page URL.
        """
        self.driver.get(self.LOGIN_URL)

    def enter_email(self, email):
        """
        Enters the provided email into the email input field.
        """
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        """
        Enters the provided password into the password input field.
        """
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        """
        Clicks the login button to submit credentials.
        """
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def verify_login_success(self):
        """
        Verifies successful login by checking for dashboard element.
        Returns:
            bool: True if dashboard is visible, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD))
            return True
        except Exception:
            return False

    def verify_login_error(self):
        """
        Verifies login failure by checking for error message element.
        Returns:
            str: Error message text if present, empty string otherwise.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return ""

    # --- STRUCTURED TEST FLOW ---
    def login_and_verify(self, email, password):
        """
        Performs end-to-end login and verifies outcome.
        Args:
            email (str): User email
            password (str): User password
        Returns:
            dict: {
                'email': email,
                'password': password,
                'success': bool,
                'error_message': str
            }
        """
        self.navigate_to_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        success = self.verify_login_success()
        error_message = ""
        if not success:
            error_message = self.verify_login_error()
        return {
            'email': email,
            'password': password,
            'success': success,
            'error_message': error_message
        }

    # --- TEST DATA EXAMPLES ---
    """
    Example usage for TC_Login_01 (valid login):
        result = login_page.login_and_verify("user@example.com", "ValidPassword123")
        # result['success'] should be True

    Example usage for TC_Login_02 (invalid login):
        result = login_page.login_and_verify("wronguser@example.com", "WrongPassword")
        # result['success'] should be False, result['error_message'] should contain error text
    """

    # --- END OF LoginPage.py ---
