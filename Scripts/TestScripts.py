import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestScripts(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # ... existing test methods ...

    def test_TC_Login_05_empty_email_and_password(self):
        # Existing test implementation
        pass

    def test_TC_Login_06_remember_me_session_persistence(self):
        # Existing test implementation
        pass

    def test_TC_Login_07_session_expiration_without_remember_me(self):
        """
        TC_Login_07: Navigate to login page, enter valid credentials without 'Remember Me', click login, close and reopen browser, navigate to site, assert session expired (user is logged out).
        """
        valid_username = "user@example.com"
        valid_password = "ValidPassword123"
        # Step 1: Navigate to login page (already handled in setUp)
        # Step 2: Enter valid credentials without selecting 'Remember Me'
        self.login_page.enter_username(valid_username)
        self.login_page.enter_password(valid_password)
        # Ensure 'Remember Me' is not selected
        self.assertFalse(self.login_page.is_remember_me_selected(), "'Remember Me' should NOT be selected")
        # Step 3: Click the 'Login' button
        self.login_page.click_login()
        # Assert user is logged in
        self.assertTrue(self.login_page.is_login_successful(), "User should be logged in after valid credentials")
        # Step 4: Close and reopen browser; navigate to site
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/")
        self.login_page = LoginPage(self.driver)
        # Assert user is logged out (session expired)
        session_expired = self.login_page.verify_session_expiration()
        self.assertTrue(session_expired, "Session should be expired and user logged out after browser restart without 'Remember Me'")
        self.driver.quit()
        self.driver = None

    def test_TC_LOGIN_001_valid_login_dashboard_redirect(self):
        """
        TC_LOGIN_001: Navigate to login page, enter valid email/username and password, click login, assert user is redirected to dashboard.
        """
        valid_username = "user@example.com"
        valid_password = "ValidPassword123"
        # Step 1: Navigate to login page (already handled in setUp)
        # Step 2: Enter valid email/username and valid password
        self.login_page.enter_username(valid_username)
        self.login_page.enter_password(valid_password)
        # Step 3: Click the Login button
        self.login_page.click_login()
        # Assert user is redirected to dashboard
        self.assertTrue(self.login_page.is_login_successful(), "User should be redirected to dashboard after successful login")
