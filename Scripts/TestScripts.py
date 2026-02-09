import unittest
from RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage
from Pages.ForgotPasswordPage import ForgotPasswordPage
from selenium import webdriver

class TestRuleConfiguration(unittest.TestCase):
    # ... (existing test methods and logic remain unchanged)
    pass

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC_SCRUM158_09_malicious_metadata(self):
        """
        TC_SCRUM158_09: Prepare a schema with malicious metadata and submit. Expect rejection and error.
        """
        schema = {
            "trigger": {"type": "manual"},
            "conditions": [{"type": "amount", "operator": "==", "value": 1}],
            "actions": [{"type": "transfer", "account": "I", "amount": 1}],
            "metadata": "<script>alert('hack')</script>"
        }
        result, message = self.rule_page.submit_rule_with_malicious_metadata(schema)
        self.assertFalse(result)
        self.assertIn("error", message.lower())

    def test_TC_SCRUM158_10_unsupported_trigger(self):
        """
        TC_SCRUM158_10: Prepare a schema with unsupported trigger type and submit. Expect graceful rejection.
        """
        schema = {
            "trigger": {"type": "future_type"},
            "conditions": [{"type": "amount", "operator": "==", "value": 1}],
            "actions": [{"type": "transfer", "account": "J", "amount": 1}]
        }
        result, message = self.rule_page.submit_rule_with_unsupported_trigger(schema)
        self.assertFalse(result)
        self.assertTrue("error" in message.lower() or "unsupported" in message.lower())

# --- Append new test methods below ---

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC05_login_empty_password(self):
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username("valid_user")
        self.login_page.leave_password_empty()
        self.login_page.click_login_button()
        error = self.login_page.validate_error_message()
        self.assertEqual(error, "Password is required")

    def test_TC06_login_remember_me(self):
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username("valid_user")
        self.login_page.enter_password("ValidPass123")
        self.login_page.check_remember_me()
        self.login_page.click_login_button()
        self.assertTrue(self.login_page.validate_session_persistence())
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        session_persistent = self.login_page.validate_session_persistence()
        self.assertTrue(session_persistent)

# --- New Transfer API Test Cases ---

from Pages.TransferAPIPage import TransferAPIPage

class TestTransferAPIPage(unittest.TestCase):
    def setUp(self):
        # Provide the base_url as needed for your environment
        self.base_url = "https://your-app-url.com"
        self.api_page = TransferAPIPage(base_url=self.base_url)

    def test_TC_158_09_valid_transfer_and_log(self):
        """
        TC-158-09: Submit a valid transfer payload and check backend log entry.
        """
        payload = {
            "amount": 200.00,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        response = self.api_page.submit_transfer_payload(payload)
        self.assertTrue(self.api_page.validate_currency_success(response))
        confirmation = response.json().get("confirmation")
        log_entry = self.api_page.query_backend_log_entry(confirmation)
        self.assertIsNotNone(log_entry)

    def test_TC_158_10_unsupported_currency_rejection(self):
        """
        TC-158-10: Submit payload with unsupported currency, validate rejection and error message.
        """
        payload = {
            "amount": 100.00,
            "currency": "XYZ",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        response = self.api_page.submit_transfer_payload(payload)
        self.assertTrue(self.api_page.validate_currency_rejection(response))
        error_message = response.json().get("message", "")
        self.assertIn("Unsupported currency", error_message)
