
import unittest
from Pages.RuleConfigurationPage import (
    input_rule_schema_max_conditions_actions,
    input_rule_schema_empty_conditions_actions,
    submit_rule_schema,
    retrieve_and_validate_rule,
    robust_error_handling_and_schema_validation
)
from Pages.LoginPage import LoginPage
from selenium import webdriver

class TestRuleConfiguration(unittest.TestCase):

    # Existing test methods...
    # (Assume all previous content is preserved here)

    def test_TC_SCRUM158_07_create_rule_with_max_conditions_actions(self):
        """TC_SCRUM158_07: Create rule with max (10) conditions/actions and validate persistence."""
        rule_data = input_rule_schema_max_conditions_actions()
        submit_rule_schema(rule_data)
        persisted_rule = retrieve_and_validate_rule(rule_data['name'])
        self.assertEqual(len(persisted_rule['conditions']), 10, "Should have 10 conditions")
        self.assertEqual(len(persisted_rule['actions']), 10, "Should have 10 actions")
        robust_error_handling_and_schema_validation(persisted_rule)
        # Additional assertions as per business requirements can be added here

    def test_TC_SCRUM158_08_create_rule_with_empty_conditions_actions(self):
        """TC_SCRUM158_08: Create rule with empty conditions/actions arrays and validate business rule."""
        rule_data = input_rule_schema_empty_conditions_actions()
        submit_rule_schema(rule_data)
        persisted_rule = retrieve_and_validate_rule(rule_data['name'])
        self.assertEqual(len(persisted_rule['conditions']), 0, "Should have 0 conditions")
        self.assertEqual(len(persisted_rule['actions']), 0, "Should have 0 actions")
        robust_error_handling_and_schema_validation(persisted_rule)
        # Assert business rule: e.g., rule may not be active, or must show validation error depending on requirements
        # If business rule expects error, add:
        # self.assertIn('error', persisted_rule)

class TestLogin(unittest.TestCase):
    """
    Test cases for Login functionality using LoginPage Page Object.
    """
    def setUp(self):
        self.driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc.
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC_Login_01_valid_login(self):
        """
        TC_Login_01: Valid login with user@example.com / ValidPassword123
        Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Click login
        4. Verify dashboard loaded
        """
        result = self.login_page.login_and_verify("user@example.com", "ValidPassword123")
        self.assertTrue(result['success'], "User should be logged in and redirected to dashboard.")
        self.assertEqual(result['error_message'], "", "No error message should be displayed for valid login.")

    def test_TC_Login_02_invalid_login(self):
        """
        TC_Login_02: Invalid login with wronguser@example.com / WrongPassword
        Steps:
        1. Navigate to login page
        2. Enter invalid credentials
        3. Click login
        4. Verify error message displayed, user not logged in
        """
        result = self.login_page.login_and_verify("wronguser@example.com", "WrongPassword")
        self.assertFalse(result['success'], "User should not be logged in with invalid credentials.")
        self.assertNotEqual(result['error_message'], "", "Error message should be displayed for invalid login.")

    def test_TC_Login_03_missing_email(self):
        """
        TC_Login_03: Missing email, valid password
        Steps:
        1. Navigate to login page
        2. Leave email empty, enter valid password
        3. Click login
        4. Expect error 'Email required', user not logged in
        """
        result = self.login_page.login_and_verify("", "ValidPassword123")
        self.assertFalse(result['success'], "User should not be logged in when email is missing.")
        self.assertTrue(result['email_required'], "'Email required' error should be displayed.")
        self.assertEqual(result['error_message'], "Email required", "Error message should be 'Email required'.")

    def test_TC_Login_04_missing_password(self):
        """
        TC_Login_04: Valid email, missing password
        Steps:
        1. Navigate to login page
        2. Enter valid email, leave password empty
        3. Click login
        4. Expect error 'Password required', user not logged in
        """
        result = self.login_page.login_and_verify("user@example.com", "")
        self.assertFalse(result['success'], "User should not be logged in when password is missing.")
        self.assertTrue(result['password_required'], "'Password required' error should be displayed.")
        self.assertEqual(result['error_message'], "Password required", "Error message should be 'Password required'.")

    def test_TC_LOGIN_002_invalid_credentials(self):
        """
        TC_LOGIN_002: Enter invalid credentials and verify error message
        Steps:
        1. Navigate to login page
        2. Enter invalid email/username or password (wronguser@example.com / WrongPassword)
        3. Click login
        4. Verify error message displayed for invalid credentials
        """
        self.login_page.login_with_credentials("wronguser@example.com", "WrongPassword")
        error_message = self.login_page.get_error_message()
        self.assertIsNotNone(error_message, "Error message should be displayed for invalid credentials.")
        self.assertIn("Invalid credentials", error_message, "Error message should indicate invalid credentials.")

    def test_TC_LOGIN_003_empty_fields(self):
        """
        TC_LOGIN_003: Leave fields empty and verify error message
        Steps:
        1. Navigate to login page
        2. Leave email/username and password fields empty ('', '')
        3. Click login
        4. Verify error or validation message for empty fields is displayed
        """
        email_error = self.login_page.validate_missing_email_error("")
        password_error = self.login_page.validate_missing_password_error("")
        self.assertTrue(email_error, "Missing email error should be displayed when email is empty.")
        self.assertTrue(password_error, "Missing password error should be displayed when password is empty.")
