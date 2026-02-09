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
