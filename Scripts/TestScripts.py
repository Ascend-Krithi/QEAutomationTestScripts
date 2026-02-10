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
        '''
        Implements all steps for TC-SCRUM-158-001:
        1. Prepare rule JSON with two triggers, two conditions, two actions, and metadata.
        2. Submit to JSON Schema validation endpoint.
        3. Serialize to JSON string and verify.
        4. Deserialize and verify.
        5. Submit to evaluation service and measure response time.
        6. Verify response time <= 200ms.
        7. Query DB to verify storage.
        8. Perform security validation with malicious payloads.
        9. Retrieve rule via API and verify.
        '''
        rule_json = {
            "rule_id": "RULE-001",
            "rule_name": "Multi-Condition Savings Rule",
            "enabled": True,
            "priority": 1,
            "user_id": "USER-12345",
            "triggers": [
                {"type": "specific_date", "date": "2024-06-01T00:00:00Z"},
                {"type": "recurring_interval", "interval": "MONTHLY", "day_of_month": 1}
            ],
            "conditions": [
                {"type": "balance_threshold", "operator": "greater_than", "value": 1000.00, "currency": "USD"},
                {"type": "transaction_source", "source_type": "DIRECT_DEPOSIT"}
            ],
            "actions": [
                {"type": "fixed_amount", "amount": 50.00, "currency": "USD", "target_account": "savings_001"},
                {"type": "percentage_of_deposit", "percentage": 10.0, "target_account": "investment_001"}
            ]
        }
        # Step 1: Fill form and submit
        self.rule_page.fill_rule_form(rule_json)
        validation_status, validation_result = self.rule_page.validate_rule_schema(rule_json)
        assert validation_status == 200, f"Validation endpoint returned {validation_status}"
        assert validation_result.get('validation_result') == 'PASSED', f"Validation failed: {validation_result}"
        # Step 2: Serialize
        serialized = self.rule_page.serialize_rule(rule_json)
        assert isinstance(serialized, str), "Serialization failed"
        # Step 3: Deserialize
        deserialized = self.rule_page.deserialize_rule(serialized)
        assert deserialized == rule_json, "Deserialization did not match original"
        # Step 4: Submit to evaluation service
        auth_token = "BearerTokenStub"
        eval_status, eval_result, processing_time = self.rule_page.submit_rule_to_evaluation_service(rule_json, auth_token)
        assert eval_status == 201, f"Evaluation service returned {eval_status}"
        assert processing_time <= 0.2 or float(processing_time) <= 0.2, f"Processing time exceeded 200ms: {processing_time}"
        # Step 5: DB verification
        db_result = self.rule_page.query_database_for_rule("RULE-001")
        assert db_result, "Database did not return rule"
        # Step 6: Security validation
        malicious_payloads = [
            {"rule_name": "<script>alert(1)</script>"},
            {"conditions": [{"value": "1000 OR 1=1"}]},
            {"actions": [{"parameter": "'; DROP TABLE rules;--"}]}
        ]
        for payload in malicious_payloads:
            status, result = self.rule_page.perform_security_validation(payload)
            assert status in [200, 400], f"Unexpected status for security validation: {status}"
            assert not any(["vulnerability" in str(result).lower(), "error" in str(result).lower()]), "Security validation failed"
        # Step 7: Retrieve via API
        retrieve_status, retrieve_result = self.rule_page.retrieve_rule_via_api("RULE-001", auth_token)
        assert retrieve_status == 200, f"Retrieve API returned {retrieve_status}"
        assert retrieve_result.get("rule_id") == "RULE-001", "Rule ID mismatch in API retrieval"

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
