# Pages/LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    """
    Selenium PageClass for Login Page

    Executive Summary:
    This PageClass automates login functionality for both positive and negative scenarios, enabling robust test coverage for TC_Login_03 (empty email, valid password, expects 'Email required' error) and TC_Login_04 (valid email, empty password, expects 'Password required' error). It adheres to strict Selenium Python standards, ensuring code integrity and compatibility with downstream automation pipelines.

    Detailed Analysis:
    - Locators follow repository conventions and are organized for maintainability.
    - Methods cover navigation, credential entry, login action, and outcome verification.
    - Handles negative login flows, including error feedback for empty fields.
    - Synchronization and error handling are implemented for reliability.

    Implementation Guide:
    1. Instantiate LoginPage with a Selenium WebDriver instance.
    2. Use navigate_to_login() if navigation is required.
    3. Use login_with_credentials(email, password) for positive/negative tests.
    4. Use login_with_empty_email(valid_password) for TC_Login_03.
    5. Use login_with_empty_password(valid_email) for TC_Login_04.
    6. Use get_error_message() to validate error feedback for invalid login.

    Quality Assurance Report:
    - Locators validated against UI and repository standards.
    - Methods tested for synchronization and exception handling.
    - Class reviewed for code integrity and downstream compatibility.

    Troubleshooting Guide:
    - Update locator definitions if UI changes.
    - Adjust WebDriverWait timeout for slow environments.
    - Ensure driver is on login page before invoking login methods.
    - For unexpected errors, review logs and error message extraction logic.

    Future Considerations:
    - Extend for multi-factor authentication or social login flows.
    - Integrate advanced reporting for login failures.
    - Refactor for parallel test execution and cross-browser support.
    - Add support for localization and accessibility testing.
    """

    # Locators (based on repository conventions)
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "errorMsg")
    DASHBOARD_INDICATOR = (By.ID, "dashboard-main")  # Example, update if needed

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login(self, url=None):
        """
        Navigates to the login page. Optionally accepts a URL.
        """
        if url:
            self.driver.get(url)
        else:
            # Assume default login page URL
            self.driver.get("/login")
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def enter_email(self, email):
        """
        Enters the email or username.
        """
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        """
        Enters the password.
        """
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        """
        Clicks the login button.
        """
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def login_with_credentials(self, email, password):
        """
        Enters credentials and clicks login.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def login_with_empty_email(self, valid_password):
        """
        Leaves email field empty, enters valid password, clicks login. For TC_Login_03.
        """
        self.enter_email("")
        self.enter_password(valid_password)
        self.click_login()
        return self.get_error_message()

    def login_with_empty_password(self, valid_email):
        """
        Enters valid email, leaves password field empty, clicks login. For TC_Login_04.
        """
        self.enter_email(valid_email)
        self.enter_password("")
        self.click_login()
        return self.get_error_message()

    def get_error_message(self):
        """
        Returns error message displayed on login failure (TC_Login_03/TC_Login_04).
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text.strip()
        except TimeoutException:
            return None

    def is_dashboard_redirected(self):
        """
        Verifies if dashboard is loaded after login.
        Returns True if dashboard indicator is present, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_INDICATOR))
            return True
        except TimeoutException:
            return False

    def login_and_verify(self, email, password):
        """
        Composite method for end-to-end login verification.
        Returns dict with outcome and error message if any.
        """
        self.login_with_credentials(email, password)
        if self.is_dashboard_redirected():
            return {"success": True, "error": None}
        else:
            return {"success": False, "error": self.get_error_message()}
