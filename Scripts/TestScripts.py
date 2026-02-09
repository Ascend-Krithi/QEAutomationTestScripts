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
