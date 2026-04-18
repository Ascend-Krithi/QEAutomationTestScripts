import pytest
from Pages.RuleConfigurationPage import RuleConfigurationPage
@pytest.mark.tc_scrum158_01
def test_create_and_verify_rule():
    page = RuleConfigurationPage()
    page.create_and_verify_rule()
@pytest.mark.tc_scrum158_02
def test_create_and_verify_rule_with_specific_trigger():
    page = RuleConfigurationPage()
    page.create_and_verify_rule_with_specific_trigger()
@pytest.mark.tc_scrum158_03
def test_create_and_verify_recurring_interval_rule():
    page = RuleConfigurationPage()
    page.create_and_verify_recurring_interval_rule()
@pytest.mark.tc_scrum158_04
def test_verify_error_for_missing_trigger():
    page = RuleConfigurationPage()
    page.verify_error_for_missing_trigger()
@pytest.mark.tc_scrum158_01
def test_TC_SCRUM158_01(driver):
    '''Test Case TC_SCRUM158_01: Valid rule schema creation.'''
    schema = {
        "trigger": {"type": "interval", "value": "daily"},
        "conditions": [{"type": "amount", "operator": ">", "value": 100}],
        "actions": [{"type": "transfer", "account": "A", "amount": 100}]
    }
    page = RuleConfigurationPage(driver)
    page.fill_rule_schema(schema)
    page.submit_rule()
    assert page.validate_rule_creation(), "Rule creation failed for TC_SCRUM158_01"
@pytest.mark.tc_scrum158_02
def test_TC_SCRUM158_02(driver):
    '''Test Case TC_SCRUM158_02: Rule schema with two conditions and two actions.'''
    schema = {
        "trigger": {"type": "manual"},
        "conditions": [
            {"type": "amount", "operator": ">", "value": 500},
            {"type": "country", "operator": "==", "value": "US"}
        ],
        "actions": [
            {"type": "transfer", "account": "B", "amount": 500},
            {"type": "notify", "message": "Transfer complete"}
        ]
    }
    page = RuleConfigurationPage(driver)
    page.fill_rule_schema(schema)
    page.submit_rule()
    assert page.validate_rule_creation(), "Rule creation failed for TC_SCRUM158_02"
@pytest.mark.tc_scrum158_07
def test_TC_SCRUM158_07(driver):
    '''Test Case TC_SCRUM158_07: Minimal schema test (one trigger, one condition, one action).'''
    schema = {
        "trigger": {"type": "manual"},
        "conditions": [{"type": "amount", "operator": "==", "value": 1}],
        "actions": [{"type": "transfer", "account": "G", "amount": 1}]
    }
    page = RuleConfigurationPage(driver)
    page.fill_rule_schema(schema)
    page.submit_rule()
    assert page.validate_rule_creation(), "Rule creation failed for TC_SCRUM158_07"
@pytest.mark.tc_scrum158_08
def test_TC_SCRUM158_08(driver):
    '''Test Case TC_SCRUM158_08: Large metadata field test (10,000+ chars).'''
    schema = {
        "trigger": {"type": "manual"},
        "metadata": ""}

@pytest.mark.tc_scrum158_05
def test_TC_SCRUM158_05(driver):
    '''
    Test Case TC_SCRUM158_05: Schema with unsupported trigger type.
    '''
    schema = {
        "trigger": {"type": "unsupported_type"},
        "conditions": [{"type": "amount", "operator": "<", "value": 10}],
        "actions": [{"type": "transfer", "account": "E", "amount": 10}]
    }
    page = RuleConfigurationPage(driver)
    error_message = page.submit_schema_with_unsupported_trigger(str(schema))
    assert "unsupported" in error_message.lower(), "Expected error message for unsupported trigger type"

@pytest.mark.tc_scrum158_06
def test_TC_SCRUM158_06(driver):
    '''
    Test Case TC_SCRUM158_06: Schema with maximum allowed conditions and actions.
    '''
    schema = {
        "trigger": {"type": "manual"},
        "conditions": [
            {"type": "amount", "operator": "==", "value": 1},
            {"type": "amount", "operator": "==", "value": 2},
            {"type": "amount", "operator": "==", "value": 3},
            {"type": "amount", "operator": "==", "value": 4},
            {"type": "amount", "operator": "==", "value": 5},
            {"type": "amount", "operator": "==", "value": 6},
            {"type": "amount", "operator": "==", "value": 7},
            {"type": "amount", "operator": "==", "value": 8},
            {"type": "amount", "operator": "==", "value": 9},
            {"type": "amount", "operator": "==", "value": 10}
        ],
        "actions": [
            {"type": "transfer", "account": "F1", "amount": 1},
            {"type": "transfer", "account": "F2", "amount": 2},
            {"type": "transfer", "account": "F3", "amount": 3},
            {"type": "transfer", "account": "F4", "amount": 4},
            {"type": "transfer", "account": "F5", "amount": 5},
            {"type": "transfer", "account": "F6", "amount": 6},
            {"type": "transfer", "account": "F7", "amount": 7},
            {"type": "transfer", "account": "F8", "amount": 8},
            {"type": "transfer", "account": "F9", "amount": 9},
            {"type": "transfer", "account": "F10", "amount": 10}
        ]
    }
    page = RuleConfigurationPage(driver)
    success_message = page.submit_schema_with_max_conditions_actions(str(schema))
    assert "success" in success_message.lower(), "Expected success message for maximum allowed conditions/actions"
