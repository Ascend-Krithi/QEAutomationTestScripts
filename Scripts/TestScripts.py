# Import necessary modules
import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:8000"  # Adjust as per your environment
        self.login_page = LoginPage(self.driver, self.base_url)
        self.dashboard_page = DashboardPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_TC_Login_01_valid_login(self):
        ...
    def test_TC_Login_02_invalid_login(self):
        ...
    async def test_empty_fields_validation(self):
        ...
    async def test_remember_me_functionality(self):
        ...
    def test_TC_Login_03_empty_email(self):
        ...
    def test_TC_Login_04_empty_password(self):
        ...

    def test_TC_Login_05_empty_fields(self):
        """
        TC_Login_05: Navigates to login, leaves fields empty, attempts login, asserts error messages for both fields, and asserts user is not logged in.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        email_error = self.login_page.get_email_error()
        password_error = self.login_page.get_password_error()
        assert email_error is not None and email_error != "", "Email error message should be displayed"
        assert password_error is not None and password_error != "", "Password error message should be displayed"
        assert not self.dashboard_page.is_logged_in(), "User should not be logged in with empty fields"

    def test_TC_Login_06_remember_me_session_persistence(self):
        """
        TC_Login_06: Navigates to login, enters valid credentials, selects Remember Me, logs in, asserts user is logged in, closes and reopens browser, navigates to site, asserts session persists (user remains logged in).
        """
        valid_email = "user@example.com"
        valid_password = "securePassword123"
        self.login_page.navigate_to_login()
        self.login_page.enter_email(valid_email)
        self.login_page.enter_password(valid_password)
        self.login_page.select_remember_me()
        self.login_page.click_login()
        assert self.dashboard_page.is_logged_in(), "User should be logged in after valid login with Remember Me"
        # Save cookies for session persistence
        cookies = self.driver.get_cookies()
        self.driver.quit()
        # Reopen browser and set cookies
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.dashboard_page = DashboardPage(self.driver)
        assert self.dashboard_page.is_logged_in(), "User session should persist with Remember Me after browser restart"

# Additional classes and methods follow...
