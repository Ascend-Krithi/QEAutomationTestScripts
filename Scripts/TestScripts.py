import unittest
from RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage
from Pages.ForgotPasswordPage import ForgotPasswordPage
from selenium import webdriver
from Pages.TransferAPIPage import TransferAPIPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()

    # Existing test methods...

    def test_TC_SCRUM158_01(self):
        ...
    # (all other methods as above)

    def test_TC03_login_empty_credentials(self):
        ...
    def test_TC04_login_empty_username(self):
        ...

    def test_TC05_login_empty_password(self):
        ...
    def test_TC06_login_remember_me(self):
        ...
    def test_TC07_forgot_password_flow(self):
        ...
    def test_TC08_login_max_length_credentials(self):
        ...

    def test_TC09_login_with_special_characters(self):
        """TC09: Navigate to login page, enter username and password with special characters, click login, validate login or error."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.navigate_to_login_page("http://example.com/login")  # Replace with actual URL
            login_page.login_with_special_characters("user!@#", "pass$%^&*")
            # Validate login success or error
            error_message = login_page.get_error_message()
            if error_message:
                # If error is expected for invalid credentials
                self.assertIn("Invalid", error_message)
            else:
                # If login is successful, validate post-login condition if possible
                self.assertIsNone(error_message, "Unexpected error message displayed.")
        finally:
            driver.quit()

    def test_TC10_login_network_failure(self):
        """TC10: Navigate to login page, enter valid credentials, simulate network/server error during login, validate error message."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.navigate_to_login_page("http://example.com/login")  # Replace with actual URL
            login_page.login_with_network_failure("valid_user", "ValidPass123")
            error_message = login_page.get_error_message()
            self.assertIsNotNone(error_message, "Expected error message not displayed during network/server error.")
            self.assertIn("Unable to connect", error_message)
        finally:
            driver.quit()

    # --- New API Automation Tests ---
    def test_TC158_03_transfer_minimum_amount(self):
        """TC-158-03: Submit minimum allowed amount and expect successful transfer."""
        api_page = TransferAPIPage(base_url="http://example.com/api")  # Replace with actual API base URL
        payload = {
            "amount": 0.01,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        response = api_page.submit_transfer_payload(payload)
        self.assertTrue(api_page.validate_transfer_success(response), "Transfer with minimum amount should succeed.")

    def test_TC158_04_transfer_exceed_max_amount(self):
        """TC-158-04: Submit amount exceeding maximum allowed and expect rejection."""
        api_page = TransferAPIPage(base_url="http://example.com/api")  # Replace with actual API base URL
        payload = {
            "amount": 1000000.00,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        response = api_page.submit_transfer_payload(payload)
        self.assertTrue(api_page.validate_transfer_rejection(response), "Transfer exceeding max amount should be rejected.")

if __name__ == "__main__":
    unittest.main()
