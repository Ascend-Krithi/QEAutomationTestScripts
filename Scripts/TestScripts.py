# Placeholder for new TC_LOGIN_005 and TC_LOGIN_006 tests

import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.login_url = 'https://example.com/login'  # Replace with actual login URL

    def tearDown(self):
        self.driver.quit()

    def test_TC_LOGIN_009_max_length_fields(self):
        """
        Test Case TC_LOGIN_009:
        1. Navigate to the login page.
        2. Enter maximum allowed characters in email/username and password fields.
        3. Click the 'Login' button.
        4. Validate error message and UI overflow.
        """
        self.login_page.navigate_to_login(self.login_url)
        result = self.login_page.enter_max_length_credentials()
        self.assertTrue(result, "Fields did not accept maximum allowed characters (50)")
        self.login_page.click_login()
        error_msg = self.login_page.get_error_message()
        self.assertIn(error_msg, ["Invalid credentials", "User not found"], f"Unexpected error message: {error_msg}")
        ui_ok = self.login_page.is_field_overflow()
        self.assertTrue(ui_ok, "UI overflow or break detected after max input")

    def test_TC_LOGIN_010_unregistered_user(self):
        """
        Test Case TC_LOGIN_010:
        1. Navigate to the login page.
        2. Enter email/username and password for a user not registered.
        3. Click the 'Login' button.
        4. Validate error message and ensure user remains on login page.
        """
        self.login_page.navigate_to_login(self.login_url)
        self.login_page.enter_credentials("unknown@example.com", "RandomPass789")
        self.login_page.click_login()
        error_msg = self.login_page.get_error_message()
        self.assertIn(error_msg, ["User not found", "Invalid credentials"], f"Unexpected error message: {error_msg}")
        # Optionally, check that current URL is still login page
        self.assertTrue(self.login_url in self.driver.current_url, "User did not remain on login page after failed login")

if __name__ == "__main__":
    unittest.main()
