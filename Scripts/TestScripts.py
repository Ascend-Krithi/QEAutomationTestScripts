import asyncio
from RuleConfigurationPage import RuleConfigurationPage
from LoginPage import LoginPage
from datetime import datetime, timedelta

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

# --- New Test Methods Appended Below ---

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_create_and_verify_rule_TC_SCRUM_158_001(self):
        pass

    async def test_rule_execution_and_log_TC_SCRUM_158_002(self):
        pass

    async def test_negative_rule_creation_TC_SCRUM_387_005(self):
        """
        TC-SCRUM-387-005: Attempt to create a rule with invalid/missing mandatory fields.
        Steps:
        1. Navigate to rule configuration page.
        2. Attempt to submit rule form with missing mandatory fields.
        3. Validate structured error response and error message.
        """
        await self.rule_page.navigate_to_rule_configuration()
        # Fill form with missing mandatory fields (e.g., no rule name)
        await self.rule_page.fill_rule_form(rule_name='', rule_type='')
        await self.rule_page.submit_rule_form()
        error = await self.rule_page.get_error_message()
        assert error is not None, 'Error message should be displayed for missing fields.'
        assert 'mandatory' in error.lower() or 'required' in error.lower(), f'Unexpected error message: {error}'

    async def test_negative_rule_creation_type_mismatch_TC_SCRUM_387_006(self):
        """
        TC-SCRUM-387-006: Attempt to create a rule with type-mismatched input fields.
        Steps:
        1. Navigate to rule configuration page.
        2. Fill form with invalid data types (e.g., string instead of expected integer).
        3. Submit and validate error response.
        """
        await self.rule_page.navigate_to_rule_configuration()
        # Fill form with type mismatch, e.g., threshold expects int, but string is provided
        await self.rule_page.fill_rule_form(rule_name='InvalidTypeRule', rule_type='Threshold', threshold='not_an_integer')
        await self.rule_page.submit_rule_form()
        error = await self.rule_page.get_error_message()
        assert error is not None, 'Error message should be displayed for type mismatch.'
        assert 'type' in error.lower() or 'invalid' in error.lower(), f'Unexpected error message: {error}'

# --- TC-SCRUM-387-009: Negative and minimal valid rule creation ---

import pytest

@pytest.mark.asyncio
async def test_rule_creation_empty_triggers_conditions_actions(rule_config_page: RuleConfigurationPage):
    '''
    TC-SCRUM-387-009-Step1: Attempt to create a rule with empty triggers, conditions, and actions.
    Expects validation errors for missing required fields.
    '''
    await rule_config_page.open()
    await rule_config_page.fill_rule_form(
        rule_name="RuleEmptyFields",
        triggers=[],
        conditions=[],
        actions=[]
    )
    await rule_config_page.submit_rule()
    errors = await rule_config_page.get_validation_errors()
    assert "triggers" in errors, "Expected validation error for empty triggers"
    assert "conditions" in errors, "Expected validation error for empty conditions"
    assert "actions" in errors, "Expected validation error for empty actions"

@pytest.mark.asyncio
async def test_rule_creation_minimal_valid(rule_config_page: RuleConfigurationPage):
    '''
    TC-SCRUM-387-009-Step2: Create a rule with minimal valid trigger, condition, and action.
    Expects successful creation and no validation errors.
    '''
    await rule_config_page.open()
    await rule_config_page.fill_and_submit_rule(
        rule_name="MinimalValidRule",
        triggers=["OnCreate"],
        conditions=["IsActive"],
        actions=["Notify"]
    )
    errors = await rule_config_page.get_validation_errors()
    assert not errors, f"Unexpected validation errors: {errors}"
    rule = await rule_config_page.get_rule_by_name("MinimalValidRule")
    assert rule is not None, "Rule was not created"
    assert rule['triggers'] == ["OnCreate"]
    assert rule['conditions'] == ["IsActive"]
    assert rule['actions'] == ["Notify"]

# --- TC-SCRUM-387-001: Positive, complex rule creation and DB/API validation ---

@pytest.mark.asyncio
async def test_rule_creation_multi_trigger_condition_action(rule_config_page: RuleConfigurationPage, db_api):
    '''
    TC-SCRUM-387-001-Step1: Create a rule with multiple triggers, conditions, and actions.
    Expects successful creation, UI confirmation, and DB/API validation.
    '''
    await rule_config_page.open()
    rule_data = {
        "rule_name": "ComplexRule",
        "triggers": ["OnUpdate", "OnDelete"],
        "conditions": ["IsVerified", "IsAdmin"],
        "actions": ["SendEmail", "LogEvent"]
    }
    await rule_config_page.fill_and_submit_rule(**rule_data)
    errors = await rule_config_page.get_validation_errors()
    assert not errors, f"Unexpected validation errors: {errors}"
    rule = await rule_config_page.get_rule_by_name("ComplexRule")
    assert rule is not None, "Rule was not created"
    assert set(rule['triggers']) == set(rule_data['triggers'])
    assert set(rule['conditions']) == set(rule_data['conditions'])
    assert set(rule['actions']) == set(rule_data['actions'])

    # DB/API validation step
    db_rule = await db_api.get_rule("ComplexRule")
    assert db_rule is not None, "Rule not found in DB/API"
    assert set(db_rule['triggers']) == set(rule_data['triggers'])
    assert set(db_rule['conditions']) == set(rule_data['conditions'])
    assert set(db_rule['actions']) == set(rule_data['actions'])

@pytest.mark.asyncio
async def test_rule_creation_and_validation_ui_db(rule_config_page: RuleConfigurationPage, db_api):
    '''
    TC-SCRUM-387-001-Step2: Validate rule creation in UI and DB/API.
    Expects rule to appear in UI list and match DB/API data.
    '''
    rule_name = "ComplexRule"
    await rule_config_page.open()
    rule_ui = await rule_config_page.get_rule_by_name(rule_name)
    rule_db = await db_api.get_rule(rule_name)
    assert rule_ui is not None, "Rule not found in UI"
    assert rule_db is not None, "Rule not found in DB/API"
    assert rule_ui['rule_name'] == rule_db['rule_name']
    assert set(rule_ui['triggers']) == set(rule_db['triggers'])
    assert set(rule_ui['conditions']) == set(rule_db['conditions'])
    assert set(rule_ui['actions']) == set(rule_db['actions'])
