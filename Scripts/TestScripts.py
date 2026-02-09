import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.ForgotPasswordPage import ForgotPasswordPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_valid_login(self):
        # Existing test method for valid login
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('validuser@example.com', 'ValidPassword')
        self.assertTrue(self.login_page.validate_login_success())

    # TC_LOGIN_002: Invalid credentials
    def test_invalid_login(self):
        """TC_LOGIN_002: Enter invalid email/username or password and verify error message."""
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('wronguser@example.com', 'WrongPassword')
        # Assert that the error message for invalid credentials is displayed
        self.assertTrue(self.login_page.validate_invalid_credentials_error())

    # TC_Login_01: Valid login, redirect to dashboard
    def test_TC_Login_01_valid_login_redirect_dashboard(self):
        """TC_Login_01: Navigate to login, enter valid credentials, expect redirect to dashboard."""
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('user@example.com', 'ValidPassword123')
        self.assertTrue(self.login_page.is_dashboard_loaded(), msg="Dashboard should be loaded after valid login.")

    # TC_Login_02: Invalid login, error message
    def test_TC_Login_02_invalid_login_error_message(self):
        """TC_Login_02: Navigate to login, enter invalid credentials, expect error message 'Invalid credentials'."""
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('wronguser@example.com', 'WrongPassword')
        error_msg = self.login_page.get_error_message()
        self.assertEqual(error_msg, 'Invalid credentials', msg="Error message should be 'Invalid credentials' for invalid login.")
        self.assertFalse(self.login_page.is_dashboard_loaded(), msg="Dashboard should NOT be loaded after invalid login.")

    # ... (other tests)

    # TC_LOGIN_007: Login without 'Remember Me', session expiration after browser restart, login state validation
    def test_TC_LOGIN_007_remember_me_and_session_expiration(self):
        """TC_LOGIN_007: Login without 'Remember Me', verify session expiration after browser restart."""
        self.login_page.navigate_to_login()
        self.login_page.uncheck_remember_me()
        self.assertFalse(self.login_page.is_remember_me_selected(), msg="'Remember Me' checkbox should not be checked.")
        self.login_page.login_with_credentials('user@example.com', 'ValidPassword123')
        self.assertTrue(self.login_page.is_logged_in(), msg="User should be logged in.")
        session_expired = self.login_page.verify_session_expiration_after_restart('https://example.com/login')
        self.assertTrue(session_expired, msg="Session should expire after browser restart (user logged out).")

    # TC_LOGIN_008: Forgot Password navigation, submission, confirmation
    def test_TC_LOGIN_008_forgot_password_flow(self):
        """TC_LOGIN_008: Click 'Forgot Password', submit recovery email, validate confirmation message."""
        self.login_page.navigate_to_login()
        self.login_page.click_forgot_password_link()
        forgot_page = ForgotPasswordPage(self.driver)
        self.assertTrue(forgot_page.is_loaded(), msg="Forgot Password page should be displayed.")
        forgot_page.submit_recovery_email('user@example.com')
        confirmation_msg = forgot_page.get_confirmation_message()
        self.assertIn('Password reset email', confirmation_msg, msg="Confirmation message should indicate password reset email sent.")
