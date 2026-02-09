import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Existing test methods...

    def test_TC_LOGIN_001_valid_login_redirect_to_dashboard(self):
        """
        TC_LOGIN_001: Valid login should redirect to dashboard.
        Steps:
        1. Navigate to login page.
        2. Enter valid credentials: username='user@example.com', password='ValidPass123'.
        3. Submit login form.
        4. Verify user is logged in and redirected to dashboard.
        """
        self.login_page.navigate_to_login()
        self.login_page.login_valid_credentials('user@example.com', 'ValidPass123')
        self.assertTrue(self.login_page.is_logged_in(), "User should be logged in and redirected to dashboard.")

    def test_TC_LOGIN_002_invalid_login_error_message(self):
        """
        TC_LOGIN_002: Invalid login should show error message 'Invalid credentials'.
        Steps:
        1. Navigate to login page.
        2. Enter invalid credentials: username='user@example.com', password='WrongPass456'.
        3. Submit login form.
        4. Verify error message 'Invalid credentials' is displayed.
        """
        self.login_page.navigate_to_login()
        self.login_page.login_invalid_credentials('user@example.com', 'WrongPass456')
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Invalid credentials', "Error message should be 'Invalid credentials' for invalid login.")
