import unittest
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.TransferAPIPage import TransferAPIPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.login_page = LoginPage()
        self.rule_page = RuleConfigurationPage()

    def test_valid_login(self):
        self.assertTrue(self.login_page.login('valid_user', 'valid_pass'))

    def test_invalid_login(self):
        self.assertFalse(self.login_page.login('invalid_user', 'invalid_pass'))

    # TC09: Login with special characters
    def test_TC09_login_with_special_characters(self):
        url = 'http://example.com/login'  # Replace with actual login URL
        self.login_page.navigate_to_login(url)
        self.login_page.enter_special_characters_username('user!@#')
        self.login_page.enter_special_characters_password('pass$%^&*')
        self.login_page.click_login()
        # Assert that fields accept special characters (implicitly tested by no exceptions)
        # Assert login is processed or proper error message is shown
        if self.login_page.is_logged_in():
            self.assertTrue(self.login_page.is_logged_in())
        else:
            error_message = self.login_page.get_error_message()
            self.assertNotEqual(error_message, '', msg='Expected error message for invalid special character login')

    # TC10: Network/server error during login
    def test_TC10_network_error_during_login(self):
        url = 'http://example.com/login'  # Replace with actual login URL
        self.login_page.navigate_to_login(url)
        self.login_page.enter_username('valid_user')
        self.login_page.enter_password('ValidPass123')
        self.login_page.simulate_network_error()
        self.login_page.click_login()
        # Assert error message for network/server error
        expected_message = 'Unable to connect. Please try again later.'
        self.assertTrue(self.login_page.validate_network_error_message(expected_message), msg='Expected network error message not found')
        self.login_page.restore_network()

class TestRuleConfiguration(unittest.TestCase):
    def setUp(self):
        self.rule_page = RuleConfigurationPage()
        self.login_page = LoginPage()
        self.login_page.login('admin', 'admin_pass')

    def test_define_rule_and_execute(self):
        response = self.rule_page.define_rule_and_handle_response('percent', 20)
        self.assertEqual(response['status'], 'success')
        deposit_result = self.rule_page.simulate_deposit(1000)
        self.assertEqual(deposit_result['transferred'], 200)

    def test_define_rule_invalid_type(self):
        response = self.rule_page.define_rule_and_handle_response('unsupported', 50)
        self.assertEqual(response['status'], 'error')
        self.assertIn('Unsupported rule type', response['message'])

    # TC-FT-005: Define rule for 10% of deposit, simulate deposit, verify transfer
    def test_TC_FT_005_define_10_percent_rule_and_verify_transfer(self):
        # Step 1: Define rule for 10% of deposit
        response = self.rule_page.define_rule_and_handle_response('percent', 10)
        self.assertEqual(response['status'], 'success', msg=f"Expected success, got {response}")
        # Step 2: Simulate deposit
        deposit_amount = 5000
        deposit_result = self.rule_page.simulate_deposit(deposit_amount)
        # Step 3: Verify 10% transfer
        expected_transferred = deposit_amount * 0.10
        self.assertEqual(deposit_result['transferred'], expected_transferred, msg=f"Expected {expected_transferred}, got {deposit_result['transferred']}")
        self.assertEqual(deposit_result['status'], 'completed')

    # TC-FT-006: Define rule with unsupported type, verify graceful rejection, verify existing rules still execute
    def test_TC_FT_006_define_unsupported_rule_and_verify_rejection_and_existing_rule_execution(self):
        # Step 1: Define rule with unsupported type
        response = self.rule_page.define_rule_and_handle_response('bonus', 15)
        self.assertEqual(response['status'], 'error', msg=f"Expected error, got {response}")
        self.assertIn('Unsupported rule type', response['message'])
        # Step 2: Ensure existing rule still executes
        # Define a valid rule first
        valid_rule_response = self.rule_page.define_rule_and_handle_response('percent', 20)
        self.assertEqual(valid_rule_response['status'], 'success')
        # Simulate deposit and verify rule execution
        deposit_amount = 2000
        deposit_result = self.rule_page.simulate_deposit(deposit_amount)
        expected_transferred = deposit_amount * 0.20
        self.assertEqual(deposit_result['transferred'], expected_transferred, msg=f"Expected {expected_transferred}, got {deposit_result['transferred']}")
        self.assertEqual(deposit_result['status'], 'completed')

class TestTransferAPI(unittest.TestCase):
    def setUp(self):
        # Replace with actual API base URL and token
        self.base_url = 'https://api.example.com'
        self.auth_token = 'YOUR_AUTH_TOKEN'
        self.transfer_api = TransferAPIPage(self.base_url, self.auth_token)

    def test_TC_158_03_minimum_amount_transfer(self):
        """
        TestCase TC-158-03: Prepare JSON payload with minimum allowed amount (0.01), submit, expect success.
        """
        payload = {
            "amount": 0.01,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        result = self.transfer_api.submit_transfer(payload)
        self.assertEqual(result["status_code"], 200, f"Expected 200 OK, got {result['status_code']}")
        self.assertTrue(result["success"], f"Expected success, got {result['error_message']}")
        self.assertIn("result", result["response_json"], "Missing 'result' key in response JSON")
        self.assertEqual(result["response_json"].get("result"), "success", f"Expected 'success', got {result['response_json'].get('result')}")

    def test_TC_158_04_exceed_maximum_amount_transfer(self):
        """
        TestCase TC-158-04: Prepare JSON payload with amount exceeding maximum (1000000.00), submit, expect rejection with error message.
        """
        payload = {
            "amount": 1000000.00,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        result = self.transfer_api.submit_transfer(payload)
        self.assertFalse(result["success"], "Expected rejection for exceeding maximum amount")
        self.assertNotEqual(result["error_message"], "", "Expected error message for rejection")
        self.assertIn("Amount exceeds maximum limit", result["error_message"], f"Expected error message, got {result['error_message']}")
