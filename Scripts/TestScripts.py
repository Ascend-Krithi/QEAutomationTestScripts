import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://example.com/login')
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test methods...
    def test_TC_LOGIN_002_invalid_credentials(self): ...
    def test_TC_LOGIN_003_empty_fields(self): ...
    def test_TC_Login_10_max_length_login(self): ...
    def test_TC_LOGIN_004_max_length_login(self): ...

    def test_TC_LOGIN_007_session_expiration_after_browser_restart(self):
        # Log in with valid credentials, no 'Remember Me'
        self.login_page.login('user@example.com', 'ValidPassword123', remember_me=False)
        # Close browser
        self.driver.quit()
        # Reopen browser and navigate to login page
        self.driver = webdriver.Chrome()
        self.driver.get('https://example.com/login')
        self.login_page = LoginPage(self.driver)
        # Verify session has expired (user is logged out)
        session_expired = self.login_page.verify_session_expiration_after_browser_restart()
        self.assertTrue(session_expired, "Session should be expired after browser restart without 'Remember Me'.")

    def test_TC_LOGIN_008_forgot_password_flow(self):
        # Navigate to login page and click 'Forgot Password'
        self.login_page.forgot_password_flow('user@example.com')
        # Verify password reset confirmation message is displayed
        confirmation_displayed = self.login_page.is_password_reset_confirmation_displayed()
        self.assertTrue(confirmation_displayed, "Password reset confirmation message should be displayed.")