# Scripts/TestScripts.py
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
    '''Test Case TC_SCRUM158_07: Minimal schema - one trigger, one condition, one action.'''
    rule_id = "TC158_07"
    rule_name = "Minimal Rule"
    trigger_type = "manual"
    condition = {"type": "amount", "operator": "==", "value": 1}
    action = {"type": "transfer", "account": "G", "amount": 1}
    schema_str = '{"trigger":{"type":"manual"},"conditions":[{"type":"amount","operator":"==","value":1}],"actions":[{"type":"transfer","account":"G","amount":1}]}'
    page = RuleConfigurationPage(driver)
    success = page.create_minimal_rule(rule_id, rule_name, trigger_type, condition, action, schema_str)
    assert success is not None and "created" in success.lower(), f"Expected rule to be created successfully, got: {success}"

@pytest.mark.tc_scrum158_08
def test_TC_SCRUM158_08(driver):
    '''Test Case TC_SCRUM158_08: Large metadata field in schema.'''
    rule_id = "TC158_08"
    rule_name = "Large Metadata Rule"
    trigger_type = "manual"
    # 10,000 character metadata
    large_metadata = "x" * 10000
    schema_str = '{"trigger":{"type":"manual"},"metadata":"' + large_metadata + '"}'
    page = RuleConfigurationPage(driver)
    success, performance = page.create_rule_with_large_metadata(rule_id, rule_name, trigger_type, schema_str)
    assert success is not None and ("accepted" in success.lower() or "created" in success.lower()), f"Expected rule to be accepted if within limits, got: {success}"
    assert performance < 10, f"Performance issue: Rule creation took {performance} seconds, expected less than 10 seconds."
