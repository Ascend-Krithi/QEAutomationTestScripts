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

    # TC-FT-003: Define rule with multiple conditions, simulate deposits, verify transfer
    def test_TC_FT_003_rule_with_multiple_conditions_and_transfer_verification(self):
        # Step 1: Define rule with multiple conditions
        rule_id = 'RC003'
        rule_name = 'Salary Transfer Rule'
        trigger_type = 'after_deposit'
        conditions = [
            {"type": "balance_threshold", "operator": ">=", "value": 1000},
            {"type": "transaction_source", "value": "salary"}
        ]
        action_type = 'fixed_amount'
        amount = 50
        success_msg = self.rule_page.submit_rule_with_conditions(rule_id, rule_name, trigger_type, conditions, action_type, amount)
        self.assertIn('success', success_msg.lower())

        # Step 2: Simulate deposit with balance 900, deposit 100, source 'salary' (should NOT execute transfer)
        transfer_result_900 = self.rule_page.simulate_deposit_and_verify_transfer(balance=900, deposit=100, source='salary')
        self.assertIn('not executed', transfer_result_900.lower())

        # Step 3: Simulate deposit with balance 1200, deposit 100, source 'salary' (should execute transfer)
        transfer_result_1200 = self.rule_page.simulate_deposit_and_verify_transfer(balance=1200, deposit=100, source='salary')
        self.assertIn('executed', transfer_result_1200.lower())

    # TC-FT-004: Error handling for missing trigger and unsupported action
    def test_TC_FT_004_error_handling_for_missing_trigger_and_unsupported_action(self):
        # Step 1: Submit rule with missing trigger type
        rule_name = 'Missing Trigger Rule'
        action_type = 'fixed_amount'
        amount = 100
        error_msg_missing_trigger = self.rule_page.submit_rule_missing_trigger_and_verify_error(rule_name, action_type, amount)
        self.assertIn('missing', error_msg_missing_trigger.lower())
        self.assertIn('trigger', error_msg_missing_trigger.lower())

        # Step 2: Submit rule with unsupported action type
        rule_id = 'RC004'
        rule_name = 'Unsupported Action Rule'
        trigger_type = 'specific_date'
        unsupported_action_type = 'unknown_action'
        error_msg_unsupported_action = self.rule_page.submit_rule_with_unsupported_action_and_verify_error(rule_id, rule_name, trigger_type, unsupported_action_type)
        self.assertIn('unsupported', error_msg_unsupported_action.lower())
        self.assertIn('action', error_msg_unsupported_action.lower())

class TestTransferAPI(unittest.TestCase):
    def setUp(self):
        # Replace with actual API base URL and token
        self.base_url = 'https://api.example.com'
        self.auth_token = 'YOUR_AUTH_TOKEN'
        self.transfer_api = TransferAPIPage(self.base_url, self.auth_token)

    def test_TC_158_01_valid_financial_transfer(self):
        """
        TC-158-01: Prepare a valid JSON payload for financial transfer with all required fields, submit to /transfer endpoint, and verify successful processing.
        """
        result = self.transfer_api.submit_valid_financial_transfer()
        self.assertEqual(result['status_code'], 200, f"Expected 200 OK, got {result['status_code']}")
        self.assertTrue(result['success'], f"Expected success, got {result['error_message']}")

    def test_TC_158_02_missing_destination_transfer(self):
        """
        TC-158-02: Prepare a JSON payload missing the 'destination' field, submit to /transfer endpoint, and verify error response 'Missing required field: destination'.
        """
        result = self.transfer_api.submit_missing_destination_transfer()
        self.assertFalse(result['success'], "Expected rejection for missing destination")
        self.assertEqual(result['error_message'], "Missing required field: destination", f"Expected error message, got {result['error_message']}")
