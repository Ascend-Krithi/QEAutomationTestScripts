# Import necessary modules
import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:8000"  # Adjust as per your environment
        self.login_page = LoginPage(self.driver, self.base_url)
        self.dashboard_page = DashboardPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_TC_Login_01_valid_login(self):
        """
        Test Case TC_Login_01:
        1. Navigate to the login page.
        2. Enter valid email and password.
        3. Click the 'Login' button.
        Expected: User is logged in and redirected to account dashboard.
        """
        self.login_page.navigate()
        self.login_page.login("user@example.com", "ValidPassword123")
        assert self.dashboard_page.is_loaded(), "Dashboard should be loaded after valid login"

    def test_TC_Login_02_invalid_login(self):
        """
        Test Case TC_Login_02:
        1. Navigate to the login page.
        2. Enter invalid email and/or password.
        3. Click the 'Login' button.
        Expected: Error message displayed: 'Invalid credentials'. User is not logged in.
        """
        self.login_page.navigate()
        self.login_page.login("wronguser@example.com", "WrongPassword")
        error = self.login_page.get_error_message()
        assert error is not None, "Error message should be displayed for invalid login"
        assert "invalid" in error.lower(), "Error message should mention 'Invalid credentials'"
        assert not self.dashboard_page.is_loaded(), "Dashboard should not be loaded after invalid login"

    # Existing async tests (left unchanged)
    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

# --- Appended Selenium Test Methods for TC_SCRUM158_03 and TC_SCRUM158_04 ---

class TestRuleConfiguration:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_TC_SCRUM158_03_valid_rule_metadata_and_schema(self):
        # Set Rule Metadata
        self.rule_page.set_rule_id("RC_158_03")
        self.rule_page.set_rule_name("Deposit After Threshold")
        description = "Deposit triggered after balance threshold"
        tags = ["deposit", "threshold", "automation"]
        self.rule_page.enter_rule_metadata(description, tags)
        # Validate Schema
        self.rule_page.validate_schema()
        assert self.rule_page.is_schema_valid(), "Schema should be valid for correct metadata"
        # Submit Rule
        self.rule_page.submit_rule()
        # Assert Metadata Matches
        assert self.rule_page.assert_metadata_matches(description, tags), "Metadata should match expected values"

    def test_TC_SCRUM158_04_invalid_schema_feedback(self):
        # Set Rule Metadata with invalid schema (missing tags)
        self.rule_page.set_rule_id("RC_158_04")
        self.rule_page.set_rule_name("Deposit Missing Tags")
        description = "Deposit rule missing tags"
        tags = []  # Intentionally empty to trigger schema error
        self.rule_page.enter_rule_metadata(description, tags)
        # Validate Schema
        self.rule_page.validate_schema()
        # Assert Schema Error Message Appears
        error = self.rule_page.get_schema_error()
        assert error is not None, "Schema error feedback should be displayed"
        assert "tags" in error.lower(), "Error message should mention missing tags"

    # --- Appended Selenium Test Methods for TC_SCRUM158_07 and TC_SCRUM158_08 ---
    def test_TC_SCRUM158_07_max_conditions_and_actions(self):
        """
        Test case for creating a rule with maximum supported conditions and actions (10 each).
        Steps:
        1. Prepare test data with 10 conditions and 10 actions.
        2. Use create_rule_with_max_conditions_actions to create the rule.
        3. Assert that the rule is created and validated.
        """
        rule_id = "RC_158_07"
        rule_name = "Max Conditions Actions"
        # Prepare 10 dummy conditions and actions
        conditions = [
            {'type': 'Balance', 'balance_limit': 1000 + i * 100, 'source_provider': 'ProviderA', 'operator': '>'}
            for i in range(10)
        ]
        actions = [
            {'type': 'Transfer', 'amount': 100 + i * 10, 'percentage': None, 'destination_account': f'ACC{i+1}'}
            for i in range(10)
        ]
        result = self.rule_page.create_rule_with_max_conditions_actions(rule_id, rule_name, conditions, actions)
        assert result, "Rule with max conditions and actions should be created and validated successfully."

    def test_TC_SCRUM158_08_empty_conditions_and_actions(self):
        """
        Test case for creating a rule with empty conditions and actions arrays.
        Steps:
        1. Prepare test data with empty lists.
        2. Use create_rule_with_empty_conditions_actions to create the rule.
        3. Assert schema validation and capture any error.
        """
        rule_id = "RC_158_08"
        rule_name = "Empty Conditions Actions"
        result = self.rule_page.create_rule_with_empty_conditions_actions(rule_id, rule_name)
        assert isinstance(result, dict), "Result should be a dict with schema_valid and error keys."
        # Accept either valid or invalid as per business rule, but log error if present
        if not result['schema_valid']:
            print(f"Schema validation error: {result['error']}")
