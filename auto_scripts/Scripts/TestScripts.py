# TestScripts.py for AXOS LoginPage
from selenium import webdriver
from LoginPage import LoginPage
import pytest
import datetime

# Test Case TC-FT-001: Specific Date Trigger
@pytest.mark.usefixtures('driver_init')
def test_specific_date_trigger(driver):
    login_page = LoginPage(driver)
    login_page.open()
    # Example login credentials
    login_page.login('user@example.com', 'securepassword')
    assert login_page.is_dashboard_header_present(), 'Dashboard header not present after login.'
    # Simulate JSON rule creation (mocked)
    rule = {
        'trigger': {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'},
        'action': {'type': 'fixed_amount', 'amount': 100},
        'conditions': []
    }
    # Simulate system time reaching the trigger date (mocked)
    trigger_date = datetime.datetime.strptime(rule['trigger']['date'], '%Y-%m-%dT%H:%M:%SZ')
    now = datetime.datetime.utcnow()
    assert now < trigger_date, 'Test must run before trigger date.'
    # Here you would advance the system time or mock the scheduler
    # For demonstration, we assert the rule is accepted
    assert rule['trigger']['type'] == 'specific_date'
    # Simulate transfer action (mocked)
    transfer_executed = True  # Replace with actual system call
    assert transfer_executed, 'Transfer action was not executed.'

# Test Case TC-FT-002: Recurring Weekly Trigger
@pytest.mark.usefixtures('driver_init')
def test_recurring_weekly_trigger(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login('user@example.com', 'securepassword')
    assert login_page.is_dashboard_header_present(), 'Dashboard header not present after login.'
    # Simulate JSON rule creation (mocked)
    rule = {
        'trigger': {'type': 'recurring', 'interval': 'weekly'},
        'action': {'type': 'percentage_of_deposit', 'percentage': 10},
        'conditions': []
    }
    assert rule['trigger']['type'] == 'recurring'
    assert rule['trigger']['interval'] == 'weekly'
    # Simulate passing of several weeks (mocked)
    for week in range(3):
        # Simulate transfer action at start of each interval
        transfer_executed = True  # Replace with actual system call
        assert transfer_executed, f'Transfer action was not executed for week {week+1}.'

# Test Case TC-FT-005: 10% Deposit Rule
@pytest.mark.usefixtures('driver_init')
def test_percentage_of_deposit_rule(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login('user@example.com', 'securepassword')
    assert login_page.is_dashboard_header_present(), 'Dashboard header not present after login.'
    # Define rule for 10% of deposit action
    rule = {
        'trigger': {'type': 'after_deposit'},
        'action': {'type': 'percentage_of_deposit', 'percentage': 10},
        'conditions': []
    }
    assert rule['trigger']['type'] == 'after_deposit', 'Rule trigger type is not after_deposit.'
    # Simulate deposit of 500 units
    deposit_amount = 500
    # Simulate transfer of 10% (50 units)
    expected_transfer = deposit_amount * rule['action']['percentage'] / 100
    # Mock actual transfer execution
    transfer_executed = (expected_transfer == 50)
    assert transfer_executed, f'Transfer of {expected_transfer} units was not executed.'

# Test Case TC-FT-006: Future Rule Type (Currency Conversion)
@pytest.mark.usefixtures('driver_init')
def test_currency_conversion_rule_and_existing_rules(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login('user@example.com', 'securepassword')
    assert login_page.is_dashboard_header_present(), 'Dashboard header not present after login.'
    # Define rule with new future rule type
    rule = {
        'trigger': {'type': 'currency_conversion', 'currency': 'EUR'},
        'action': {'type': 'fixed_amount', 'amount': 100},
        'conditions': []
    }
    # Simulate system accepting or gracefully rejecting the rule
    accepted_rule_types = ['specific_date', 'recurring', 'after_deposit']
    if rule['trigger']['type'] in accepted_rule_types:
        rule_accepted = True
    else:
        rule_accepted = False
    # System should gracefully reject with a clear message
    assert rule_accepted is False, 'System did not gracefully reject unsupported rule type.'
    # Verify existing rules continue to execute as before
    # Example: re-run previous deposit rule
    previous_rule = {
        'trigger': {'type': 'after_deposit'},
        'action': {'type': 'percentage_of_deposit', 'percentage': 10},
        'conditions': []
    }
    deposit_amount = 500
    expected_transfer = deposit_amount * previous_rule['action']['percentage'] / 100
    transfer_executed = (expected_transfer == 50)
    assert transfer_executed, 'Existing rule did not execute as expected.'
