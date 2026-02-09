# TestScripts.py
import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class LoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Existing test methods...

    def test_TC09_special_character_login(self):
        """
        TC09: Login with special characters in username and password
        Acceptance Criteria:
        - Error message is shown for invalid special character input
        """
        self.login_page.navigate_to_login_page()
        username = "user!@#"
        password = "pass$%^&*"
        self.login_page.enter_special_characters(username, password)
        self.login_page.click_login_button()
        error_message = self.login_page.validate_error_message()
        self.assertIsNotNone(error_message)
        self.assertIn("Invalid characters", error_message)

    def test_TC10_network_server_error_during_login(self):
        """
        TC10: Network/server error during login
        Acceptance Criteria:
        - Error message is shown for network/server failure
        """
        self.login_page.navigate_to_login_page()
        username = "valid_user"
        password = "ValidPass123"
        self.login_page.enter_special_characters(username, password)
        self.login_page.click_login_button()
        # Simulate network failure and validate error
        error_message = self.login_page.simulate_network_failure_and_validate_error()
        self.assertIsNotNone(error_message)
        self.assertIn("Network error", error_message)

if __name__ == "__main__":
    unittest.main()
