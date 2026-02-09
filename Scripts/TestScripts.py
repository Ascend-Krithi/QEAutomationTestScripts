import unittest
from Pages.FinancialTransferPage import FinancialTransferPage
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage

class TestScripts(unittest.TestCase):
    # ... (existing methods remain unchanged)

    def test_TC_SCRUM158_09_minimum_required_fields_rule_schema(self):
        """
        TC_SCRUM158_09: Validate and submit minimum required fields rule schema.
        Steps:
          1. Prepare a rule schema with only the minimum required fields.
          2. Submit the schema.
          3. Expect: JSON schema is valid, rule is created successfully.
        """
        rule_page = RuleConfigurationPage(self.driver)
        minimum_rule_schema = {
            'trigger': 'balance_above',
            'conditions': [{ 'type': 'amount_above', 'value': 1000 }],
            'actions': [{ 'type': 'transfer', 'amount': 100 }]
        }
        # Validate schema
        is_valid = rule_page.validate_rule_schema(minimum_rule_schema)
        self.assertTrue(is_valid, "Minimum required fields rule schema should be valid.")
        # Submit schema
        response = rule_page.submit_rule_schema(minimum_rule_schema)
        self.assertEqual(response['status'], 'success', "Rule should be created successfully.")

    def test_TC_SCRUM158_10_unsupported_trigger_type(self):
        """
        TC_SCRUM158_10: Submit rule schema with unsupported trigger type and validate error response.
        Steps:
          1. Prepare a rule schema with a new, unsupported trigger type.
          2. Submit the schema.
          3. Expect: API returns appropriate error response.
        """
        rule_page = RuleConfigurationPage(self.driver)
        unsupported_rule_schema = {
            'trigger': 'future_trigger',
            'conditions': [{ 'type': 'amount_above', 'value': 2000 }],
            'actions': [{ 'type': 'transfer', 'amount': 200 }]
        }
        # Validate schema
        is_valid = rule_page.validate_rule_schema(unsupported_rule_schema)
        self.assertFalse(is_valid, "Unsupported trigger type should not be valid.")
        # Submit schema
        response = rule_page.submit_rule_schema(unsupported_rule_schema)
        self.assertEqual(response['status'], 'error', "API should return error for unsupported trigger type.")
        self.assertIn('unsupported trigger', response.get('message', '').lower(), "Error message should mention unsupported trigger.")

    def test_TC_Login_03_email_required_error(self):
        """
        TC_Login_03: Attempt login with email field empty and valid password. Expect 'Email required' error.
        Steps:
          1. Navigate to login page.
          2. Leave email field empty, enter valid password.
          3. Click Login.
          4. Assert 'Email required' error is displayed, and user is not logged in.
        """
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page("https://your-app-url/login")  # Replace with actual URL as needed
        login_page.login_with_empty_email("ValidPassword123")
        login_page.validate_email_required_error()
        self.assertFalse(login_page.is_user_logged_in(), "User should not be logged in when email is empty.")

    def test_TC_Login_04_password_required_error(self):
        """
        TC_Login_04: Attempt login with password field empty and valid email. Expect 'Password required' error.
        Steps:
          1. Navigate to login page.
          2. Enter valid email, leave password field empty.
          3. Click Login.
          4. Assert 'Password required' error is displayed, and user is not logged in.
        """
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page("https://your-app-url/login")  # Replace with actual URL as needed
        login_page.login_with_empty_password("user@example.com")
        login_page.validate_password_required_error()
        self.assertFalse(login_page.is_user_logged_in(), "User should not be logged in when password is empty.")
