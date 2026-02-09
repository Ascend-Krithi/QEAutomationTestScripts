# Scripts/TestScripts.py
import unittest
from selenium import webdriver
from Pages.FinancialTransferPage import FinancialTransferPage
from Pages.LoginPage import LoginPage
from Pages.TransferPage import TransferPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = LoginPage(self.driver)
        self.base_url = "http://localhost:8000"  # Adjust as appropriate for your environment

    def test_TC03_empty_username_and_password(self):
        """
        TC03: Submit empty username and password, expect error 'Username and password are required'.
        """
        self.page.navigate_to_login(self.base_url)
        self.page.submit_empty_credentials()
        self.assertTrue(
            self.page.validate_error_for_empty_credentials("Username and password are required"),
            "Expected error message for empty credentials not displayed."
        )

    def test_TC04_empty_username_valid_password(self):
        """
        TC04: Submit empty username and valid password, expect error 'Username is required'.
        """
        self.page.navigate_to_login(self.base_url)
        self.page.submit_empty_username_valid_password("ValidPass123")
        self.assertTrue(
            self.page.validate_error_for_empty_credentials("Username is required"),
            "Expected error message for empty username not displayed."
        )

class TestFinancialTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = FinancialTransferPage(self.driver)

    def test_TC_158_01_valid_financial_transfer(self):
        """
        TC-158-01: Valid financial transfer
        """
        confirmation = self.page.submit_transfer_payload(
            amount=100.00,
            currency='USD',
            source='ACC123',
            destination='ACC456',
            timestamp='2024-06-01T10:00:00Z'
        )
        confirmation_message = self.page.get_confirmation_message()
        self.assertIsInstance(confirmation_message, str)
        self.assertTrue(len(confirmation_message) > 0, "Confirmation message should not be empty.")

    def test_TC_158_02_invalid_transfer_missing_destination(self):
        """
        TC-158-02: Invalid transfer missing 'destination' field
        """
        self.page.submit_invalid_payload(
            amount=50.00,
            currency='USD',
            source='ACC123',
            timestamp='2024-06-01T10:00:00Z'
        )
        error_message = self.page.get_error_message()
        self.assertIsInstance(error_message, str)
        self.assertIn('destination', error_message.lower(), "Error message should mention missing 'destination'.")

class TestTransferAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # No driver needed for API tests
        cls.transfer_page = TransferPage()

    def test_TC_158_05_valid_payload_with_extra_field(self):
        """
        TC-158-05: Prepare valid JSON payload with extra 'note' field, submit to /transfer, verify acceptance.
        """
        payload = '{"amount": 100.00, "currency": "USD", "source": "ACC123", "destination": "ACC456", "timestamp": "2024-06-01T10:00:00Z", "note": "Payment for invoice #123"}'
        response = self.transfer_page.submit_json_payload(payload)
        self.assertTrue(self.transfer_page.verify_acceptance(response), f"Payload not accepted: {response}")

    def test_TC_158_06_malformed_json_payload(self):
        """
        TC-158-06: Prepare malformed JSON payload (missing closing brace), submit to /transfer, verify rejection with 'Invalid JSON format' error.
        """
        payload = '{"amount": 100.00, "currency": "USD", "source": "ACC123", "destination": "ACC456", "timestamp": "2024-06-01T10:00:00Z"'  # missing closing brace
        response = self.transfer_page.submit_json_payload(payload)
        self.assertTrue(self.transfer_page.verify_rejection(response, 'Invalid JSON format'), f"Malformed payload not rejected as expected: {response}")

# --- New Tests for Rule Configuration ---
class TestRuleConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.page = RuleConfigurationPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_TC_FT_007_bulk_rule_loading_and_evaluation(self):
        """
        TC-FT-007: Load 10,000 valid rules and trigger evaluation for all rules.
        """
        # Simulate with a small batch for demo; replace with actual 10,000 in real run
        rules_list = [
            {"trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": [{"type": "balance_threshold", "value": "1000"}]}
            for _ in range(10)  # Use 10 for demo, adjust to 10,000 for real test
        ]
        result = self.page.load_rules_in_bulk(rules_list)
        self.assertEqual(result["count"], len(rules_list), "Not all rules loaded.")
        self.assertTrue(result["elapsed"] < 300, "Bulk rule loading took too long.")  # Example threshold
        evaluation_success = self.page.trigger_evaluation_for_all_rules()
        self.assertTrue(evaluation_success, "Evaluation for all rules did not complete successfully.")

    def test_TC_FT_008_sql_injection_rejection(self):
        """
        TC-FT-008: Submit a rule with SQL injection and verify rejection.
        """
        malicious_schema = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": [{"type": "balance_threshold", "value": "1000; DROP TABLE users;--"}]
        }
        self.page.submit_rule_with_sql_injection(malicious_schema)
        rejected = self.page.validate_sql_injection_rejection()
        self.assertTrue(rejected, "SQL injection was not properly rejected.")

if __name__ == "__main__":
    unittest.main()
