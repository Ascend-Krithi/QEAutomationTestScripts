
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

    # TC_LOGIN_003: Empty fields
    def test_empty_fields_login(self):
        """TC_LOGIN_003: Leave email/username and/or password fields empty and verify error/validation message."""
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('', '')
        # Assert that the error or validation message for empty fields is displayed
        self.assertTrue(self.login_page.validate_empty_fields_error())