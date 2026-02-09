import unittest
from RuleConfigurationPage import RuleConfigurationPage
from LoginPage import LoginPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()
        self.page.open()

    def tearDown(self):
        self.page.close()

    # Existing test methods (preserved)
    # ... [existing methods here] ...

    def test_TC_SCRUM158_07_create_rule_with_required_fields(self):
        """TC_SCRUM158_07: Create rule with required fields only."""
        rule_name = "RequiredFieldsRule"
        rule_description = "Rule with only required fields"
        required_fields = {
            "name": rule_name,
            "description": rule_description,
            # Add other required fields as per PageClass definition
        }
        self.page.navigate_to_rule_creation()
        self.page.fill_rule_form(**required_fields)
        self.page.submit_rule_form()
        success_message = self.page.get_success_message()
        self.assertIn("Rule created successfully", success_message)
        rule_exists = self.page.verify_rule_exists(rule_name)
        self.assertTrue(rule_exists, "Rule should exist after creation.")

    def test_TC_SCRUM158_08_create_rule_with_large_metadata(self):
        """TC_SCRUM158_08: Create rule with large metadata."""
        rule_name = "LargeMetadataRule"
        rule_description = "Rule with large metadata"
        large_metadata = "A" * 10000  # Example: 10,000 characters
        rule_fields = {
            "name": rule_name,
            "description": rule_description,
            "metadata": large_metadata,
            # Add other required fields as per PageClass definition
        }
        self.page.navigate_to_rule_creation()
        self.page.fill_rule_form(**rule_fields)
        self.page.submit_rule_form()
        success_message = self.page.get_success_message()
        self.assertIn("Rule created successfully", success_message)
        rule_exists = self.page.verify_rule_exists(rule_name)
        self.assertTrue(rule_exists, "Rule with large metadata should exist after creation.")

class TestLoginNegativeScenarios(unittest.TestCase):
    def setUp(self):
        # Setup WebDriver and base_url here
        # Example:
        # from selenium import webdriver
        # self.driver = webdriver.Chrome()
        # self.base_url = "http://your-app-url.com"
        # For demonstration, these are placeholders
        self.driver = None
        self.base_url = "http://your-app-url.com"
        self.login_page = LoginPage(self.driver, self.base_url)

    def tearDown(self):
        # Teardown WebDriver here
        # Example:
        # if self.driver:
        #     self.driver.quit()
        pass

    def test_TC03_login_with_empty_fields(self):
        """
        TC03: Navigate to login, leave fields empty, click login, expect error 'Username and password are required'.
        """
        error_message = self.login_page.login_with_empty_fields()
        self.assertEqual(error_message, 'Username and password are required', "Expected error message for empty fields.")

    def test_TC04_login_with_empty_username(self):
        """
        TC04: Navigate to login, leave username empty, enter valid password, click login, expect error 'Username is required'.
        """
        valid_password = 'ValidPass123'
        error_message = self.login_page.login_with_empty_username(valid_password)
        self.assertEqual(error_message, 'Username is required', "Expected error message for empty username.")

    def test_TC09_login_with_special_characters(self):
        """
        TC09: Navigate to login, enter username and password with special characters, click login, expect fields accept special character input.
        """
        username = "user!@#"
        password = "pass$%^&*"
        result = self.login_page.login_with_special_characters(username, password)
        self.assertTrue(result, "Fields should accept special character input or show proper error message.")

    def test_TC10_login_with_network_failure(self):
        """
        TC10: Navigate to login, enter valid username and password, simulate network failure/server error, expect appropriate error message and login not processed.
        """
        username = "valid_user"
        password = "ValidPass123"
        # Simulate network failure
        result = self.login_page.login_with_network_failure(username, password)
        self.assertTrue(result, "Appropriate error message should be displayed for network failure.")
        # Simulate server error
        server_error_result = self.login_page.simulate_server_error()
        self.assertTrue(server_error_result, "Appropriate error message should be displayed for server error.")

if __name__ == "__main__":
    unittest.main()
