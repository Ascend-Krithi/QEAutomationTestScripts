import pytest
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
        await self.login_page.fill_email('')

class TestRuleConfigurationNegativeCases:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_invalid_trigger_value(self):
        """
        TC_SCRUM158_05: Prepare schema with invalid trigger value, submit, assert error.
        """
        await self.rule_page.navigate_to_rule_configuration()
        invalid_rule_schema = {
            "name": "Invalid Trigger Rule",
            "trigger": "INVALID_TRIGGER",  # Invalid trigger value
            "conditions": [{"type": "status", "value": "active"}],
            "actions": [{"type": "notify", "params": {"email": "test@example.com"}}]
        }
        await self.rule_page.fill_rule_schema(invalid_rule_schema)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert error_msg == "Invalid trigger value", f"Expected 'Invalid trigger value', got '{error_msg}'"

    async def test_missing_condition_parameters(self):
        """
        TC_SCRUM158_06: Prepare schema with missing condition parameters, submit, assert error.
        """
        await self.rule_page.navigate_to_rule_configuration()
        invalid_rule_schema = {
            "name": "Missing Condition Params Rule",
            "trigger": "ON_CREATE",
            "conditions": [{"type": "status"}],  # Missing 'value' parameter
            "actions": [{"type": "notify", "params": {"email": "test@example.com"}}]
        }
        await self.rule_page.fill_rule_schema(invalid_rule_schema)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert error_msg == "Condition parameters missing", f"Expected 'Condition parameters missing', got '{error_msg}'"

class TestRuleConfigurationPositiveCases:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_max_conditions_actions_schema(self):
        """
        TC_SCRUM158_07: Prepare schema with maximum supported conditions and actions (10 each), submit, validate persistence.
        """
        await self.rule_page.prepare_max_conditions_actions_schema()
        await self.rule_page.submit_max_conditions_actions_schema()
        # Assuming rule_id is available after submission
        rule_id = 'MAX_COND_ACT_RULE'  # Replace with actual retrieval if needed
        result = await self.rule_page.validate_max_conditions_actions_persistence(rule_id)
        assert result, 'Rule did not persist all conditions/actions as expected.'

    async def test_empty_conditions_actions_schema(self):
        """
        TC_SCRUM158_08: Prepare schema with empty conditions/actions, submit, validate response.
        """
        await self.rule_page.prepare_empty_conditions_actions_schema()
        await self.rule_page.submit_empty_conditions_actions_schema()
        success, message = await self.rule_page.validate_empty_conditions_actions_response()
        assert success, f'Expected schema to be valid, got error: {message}'
