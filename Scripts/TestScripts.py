import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    # Existing test methods...
    def test_login_valid_credentials(self):
        # Stub - already present
        pass

    def test_login_invalid_credentials(self):
        # Stub - already present
        pass

    def test_login_valid_redirect_dashboard(self):
        """
        TC_LOGIN_001: Positive login with valid credentials, redirect to dashboard
        Steps:
        1. Navigate to login page
        2. Enter valid email and password
        3. Click Login
        4. Validate dashboard is displayed
        """
        url = "https://your-app-url.com/login"
        email = "user@example.com"
        password = "ValidPassword123"
        self.login_page.navigate_to_login_page(url)
        self.login_page.login_with_credentials(email, password, remember_me=False)
        assert self.dashboard_page.is_on_dashboard(), "User should be redirected to dashboard after valid login"

    def test_login_without_remember_me_session_expiry(self):
        """
        TC_Login_07: Login without 'Remember Me', session expiration after browser reopen
        Steps:
        1. Navigate to login page
        2. Enter valid credentials without selecting 'Remember Me'
        3. Click Login
        4. Close and reopen browser; navigate to site
        5. Validate session expired (redirect to login)
        """
        url = "https://your-app-url.com/login"
        email = "user@example.com"
        password = "ValidPassword123"
        self.login_page.navigate_to_login_page(url)
        self.login_page.login_with_credentials(email, password, remember_me=False)
        assert self.dashboard_page.is_on_dashboard(), "User should be redirected to dashboard after login"

        # Simulate browser close and reopen
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.driver.get("https://your-app-url.com/dashboard")
        assert self.dashboard_page.is_session_expired(), "Session should expire after browser restart without 'Remember Me'. User should be redirected to login page."

    def test_forgot_password_redirect(self):
        """
        TC_Login_08: Test clicking 'Forgot Password' link and validating redirection to password recovery page.
        Steps:
        1. Navigate to login page
        2. Click the 'Forgot Password' link
        3. Validate user is redirected to password recovery page
        """
        url = "https://your-app-url.com/login"
        self.login_page.navigate_to_login_page(url)
        assert self.login_page.click_forgot_password_and_validate_redirect(), "User should be redirected to password recovery page after clicking 'Forgot Password'"

    def test_email_max_length_login(self):
        """
        TC_Login_09: Test entering maximum allowed email/username length and valid password, then clicking login and validating that the field accepts max input.
        Steps:
        1. Navigate to login page
        2. Enter 255-character email and valid password
        3. Click Login
        4. Validate field accepts max input and login succeeds
        """
        url = "https://your-app-url.com/login"
        email = "a" * 255
        password = "ValidPassword123"
        self.login_page.navigate_to_login_page(url)
        assert self.login_page.validate_email_max_length(255, email, password), "Email field should accept maximum input length of 255 characters"
