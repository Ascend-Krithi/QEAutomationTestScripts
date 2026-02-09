import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('user@example.com')
        await self.login_page.fill_password('securepassword')
        await self.login_page.toggle_remember_me()
        await self.login_page.submit_login('user@example.com', 'securepassword')
        # Add assertion for successful login and remember me
        assert await self.login_page.is_logged_in()

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_create_rule_with_invalid_trigger(self):
        """
        Test Case 1351: Attempt to create a rule with an invalid trigger value.
        Expectation: API returns 400 Bad Request and displays an error message.
        """
        self.rule_page.navigate_to_rule_configuration()
        self.rule_page.click_create_rule()
        self.rule_page.enter_rule_name('Invalid Trigger Rule')
        self.rule_page.select_trigger('invalid_trigger_value')
        self.rule_page.add_condition({'type': 'valid_type', 'params': {'key': 'value'}})
        self.rule_page.add_action({'type': 'valid_action', 'params': {'key': 'value'}})
        self.rule_page.submit_rule()
        error_message = self.rule_page.get_error_message()
        assert error_message is not None, 'Expected error message for invalid trigger'
        assert '400' in error_message or 'Bad Request' in error_message or 'invalid trigger' in error_message.lower()

    def test_create_rule_with_missing_condition_params(self):
        """
        Test Case 1352: Attempt to create a rule where a condition is missing required parameters.
        Expectation: API returns 400 Bad Request and displays an error message.
        """
        self.rule_page.navigate_to_rule_configuration()
        self.rule_page.click_create_rule()
        self.rule_page.enter_rule_name('Missing Condition Params Rule')
        self.rule_page.select_trigger('valid_trigger')
        self.rule_page.add_condition({'type': 'some_type', 'params': {}})
        self.rule_page.add_action({'type': 'valid_action', 'params': {'key': 'value'}})
        self.rule_page.submit_rule()
        error_message = self.rule_page.get_error_message()
        assert error_message is not None, 'Expected error message for missing condition parameters'
        assert '400' in error_message or 'Bad Request' in error_message or 'missing' in error_message.lower()

    def test_create_rule_with_max_conditions_actions(self):
        """
        Test Case TC_SCRUM158_07: Create rule with maximum supported conditions and actions (10 each).
        Steps:
        - Prepare a rule schema with 10 conditions and 10 actions.
        - Validate schema.
        - Submit rule.
        - Retrieve and validate all conditions/actions are persisted.
        """
        rule_id = 'max_conditions_actions_rule'
        rule_name = 'Max Conditions/Actions Rule'
        trigger_info = {'type': 'deposit'}
        conditions = [
            {'type': 'balance_above', 'threshold': 1000 + i*100, 'source': 'Bank', 'operator': 'greater_than'} for i in range(10)
        ]
        actions = [
            {'type': 'transfer', 'amount': 50 + i*10, 'destination': f'acct_{100+i}'} for i in range(10)
        ]
        schema_dict = {'trigger': 'deposit', 'conditions': conditions, 'actions': actions}
        validation_result = self.rule_page.configure_rule(rule_id, rule_name, trigger_info, conditions, actions, schema_dict)
        assert validation_result['success'] is not None, 'JSON schema should be valid.'
        assert validation_result['error'] is None, f'Unexpected schema error: {validation_result["error"]}'
        created = self.rule_page.create_rule(rule_id, rule_name, trigger_info, conditions, actions, schema_dict)
        assert created, 'Rule should be created successfully.'
        # Retrieve and validate all conditions/actions are persisted
        # This would be implemented with an API call or UI check, placeholder below:
        persisted_rule = self.rule_page.retrieve_rule(rule_id)
        assert len(persisted_rule['conditions']) == 10, 'Should persist 10 conditions.'
        assert len(persisted_rule['actions']) == 10, 'Should persist 10 actions.'

    def test_create_rule_with_empty_conditions_actions(self):
        """
        Test Case TC_SCRUM158_08: Create rule with empty conditions and actions arrays.
        Steps:
        - Prepare a rule schema with empty conditions and actions.
        - Validate schema.
        - Submit rule.
        - Check API response (error or acceptance).
        """
        rule_id = 'empty_conditions_actions_rule'
        rule_name = 'Empty Conditions/Actions Rule'
        trigger_info = {'type': 'deposit'}
        conditions = []
        actions = []
        schema_dict = {'trigger': 'deposit', 'conditions': conditions, 'actions': actions}
        validation_result = self.rule_page.configure_rule(rule_id, rule_name, trigger_info, conditions, actions, schema_dict)
        # Depending on business logic, schema may be valid or invalid
        if validation_result['success']:
            created = self.rule_page.create_rule(rule_id, rule_name, trigger_info, conditions, actions, schema_dict)
            assert created, 'Rule should be created or rejected as per business rule.'
        else:
            assert validation_result['error'] is not None, 'Expected error for empty conditions/actions.'

    # --- Appended Test Case Methods ---
    def test_TC_SCRUM158_01(self):
        """
        Test Case TC_SCRUM158_01:
        Prepare a JSON rule schema with all supported trigger, condition, and action types populated.
        [Test Data: { 'trigger': 'balance_above', 'conditions': [{...}], 'actions': [{...}] }]
        [Acceptance Criteria: TS_SCRUM158_01]
        """
        result = self.rule_page.test_TC_SCRUM158_01()
        assert result["success_message"] is not None, "Expected success message for valid schema."
        assert result["error_message"] is None, f"Unexpected error message: {result['error_message']}"
        assert result["rule_created"], "Rule should be created successfully."
        assert result["created_rule"] is not None, "Created rule should be retrieved from DB."

    def test_TC_SCRUM158_02(self):
        """
        Test Case TC_SCRUM158_02:
        Prepare a rule schema with two conditions and two actions.
        [Test Data: { 'conditions': [{...}, {...}], 'actions': [{...}, {...}] }]
        [Acceptance Criteria: TS_SCRUM158_02]
        """
        result = self.rule_page.test_TC_SCRUM158_02()
        assert result["success_message"] is not None, "Expected success message for valid schema."
        assert result["error_message"] is None, f"Unexpected error message: {result['error_message']}"
        assert result["rule_created"], "Rule should be created successfully."
        assert result["simulation_result"]["conditions_evaluated"], "Conditions should be evaluated."
        assert result["simulation_result"]["actions_executed"], "Actions should be executed."
