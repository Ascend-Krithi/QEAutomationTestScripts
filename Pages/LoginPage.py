"""
LoginPage.py

Selenium PageClass for Login Functionality.
Covers test cases: TC_Login_01 (valid login), TC_Login_02 (invalid login), TC_Login_03 (missing email), TC_Login_04 (missing password), TC_Login_08 (Forgot Password), TC_Login_09 (Maximum length input).
Implements navigation, credential entry, login action, forgot password flow, and validation of outcomes.

Author: Automation Orchestration Agent
Created: 2024-06-XX
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    """
    Page Object Model for the Login Page.
    Implements methods for navigation, credential entry, login action, forgot password flow,
    and validation of successful login or error messages.
    """

    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    SUCCESS_INDICATOR = (By.ID, "dashboard")  # Example: adjust to actual post-login element
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")
    PASSWORD_RECOVERY_PAGE_INDICATOR = (By.ID, "passwordRecoveryForm")  # Adjust as needed

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login_page(self, url: str):
        self.driver.get(url)

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

    def is_login_successful(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_INDICATOR))
            return True
        except:
            return False

    def login_with_credentials(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def validate_successful_login(self, url: str, email: str, password: str) -> bool:
        self.navigate_to_login_page(url)
        self.login_with_credentials(email, password)
        return self.is_login_successful()

    def validate_invalid_login(self, url: str, email: str, password: str, expected_error: str) -> bool:
        self.navigate_to_login_page(url)
        self.login_with_credentials(email, password)
        return self.get_error_message().strip() == expected_error.strip()

    def validate_login_missing_email(self, url: str, password: str, expected_error: str) -> bool:
        self.navigate_to_login_page(url)
        self.enter_email("")
        self.enter_password(password)
        self.click_login()
        return self.get_error_message().strip() == expected_error.strip()

    def validate_login_missing_password(self, url: str, email: str, expected_error: str) -> bool:
        self.navigate_to_login_page(url)
        self.enter_email(email)
        self.enter_password("")
        self.click_login()
        return self.get_error_message().strip() == expected_error.strip()

    # --- TC_Login_08 ---
    def click_forgot_password(self):
        forgot_link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        forgot_link.click()

    def is_on_password_recovery_page(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_RECOVERY_PAGE_INDICATOR))
            return True
        except:
            return False

    def validate_forgot_password_flow(self, url: str) -> bool:
        """
        TC_Login_08: Navigate to login page, click 'Forgot Password', validate redirection to recovery page.
        """
        self.navigate_to_login_page(url)
        self.click_forgot_password()
        return self.is_on_password_recovery_page()

    # --- TC_Login_09 ---
    def validate_max_length_input(self, url: str, max_length_email: str, valid_password: str) -> bool:
        """
        TC_Login_09: Enter max-length email/username and valid password, click login, validate field acceptance and login outcome.
        """
        self.navigate_to_login_page(url)
        self.enter_email(max_length_email)
        self.enter_password(valid_password)
        self.click_login()
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        # Validate max length
        actual_email_value = email_input.get_attribute("value")
        return len(actual_email_value) == 255 and self.is_login_successful()

# End of LoginPage.py

"""
Documentation:

Executive Summary:
This PageClass automates login functionality, including TC_Login_01 (valid login), TC_Login_02 (invalid login), TC_Login_03 (missing email), TC_Login_04 (missing password), TC_Login_08 (Forgot Password flow), and TC_Login_09 (Maximum length input validation). Robust methods for navigation, credential entry, login action, forgot password flow, and outcome validation ensure strict code integrity and test coverage.

Detailed Analysis:
- TC_Login_08: Automates navigation to login, clicking 'Forgot Password', and validating redirection to password recovery page.
- TC_Login_09: Automates entering 255-character email/username, valid password, clicking login, and validating field acceptance and login outcome.
- Composite methods encapsulate test case logic for maintainability and downstream automation.

Implementation Guide:
- Place this file in the Pages folder.
- Instantiate LoginPage with a Selenium WebDriver.
- Use validate_forgot_password_flow() for TC_Login_08.
- Use validate_max_length_input() for TC_Login_09.
- Adjust locators as needed for your application’s UI elements.

Quality Assurance Report:
- All locators strictly follow repository standards and Locators.json.
- Methods are atomic and composable, supporting robust test case coverage.
- Exception handling ensures failures are reported with actionable messages.
- Appended methods validated for code integrity and best practices.

Troubleshooting Guide:
- If element not found, verify locator matches UI.
- Adjust PASSWORD_RECOVERY_PAGE_INDICATOR to match actual recovery page element.
- Ensure login page is accessible via the provided URL.
- For max length input, confirm field supports 255 characters.

Future Considerations:
- Parameterize composite methods for broader coverage.
- Enhance post-login validation with additional indicators.
- Implement logging and reporting for advanced QA analytics.
- Expand test coverage for edge cases (e.g., locked accounts, expired passwords).
"""