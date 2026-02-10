import asyncio
from RuleConfigurationPage import RuleConfigurationPage
from ProfilePage import ProfilePage
from SettingsPage import SettingsPage
from LoginPage import LoginPage
from datetime import datetime, timedelta

class TestLoginFunctionality:
    ...
# --- New Test Methods Appended Below ---

class TestRuleConfiguration:
    ...

# --- New Async Test Methods for TC-SCRUM-158-001 and TC-SCRUM-158-002 ---

async def test_TC_SCRUM_158_001(page):
    """
    Test Case: TC-SCRUM-158-001
    Steps:
      - Navigate to Automated Transfers rule creation
      - Define a specific date trigger
      - Add balance threshold condition
      - Add fixed amount transfer action
      - Save rule
      - Retrieve rule and verify all components
    """
    rule_page = RuleConfigurationPage(page)
    await rule_page.navigate_to_rule_creation()
    await rule_page.set_trigger(trigger_type='specific_date', date='2024-12-31T10:00:00Z')
    await rule_page.add_condition(condition_type='balance_threshold', operator='greater_than', amount=500)
    await rule_page.add_action(action_type='fixed_transfer', amount=100, destination_account='SAV-001')
    await rule_page.save_rule()
    rule = await rule_page.get_rule()
    assert rule['trigger_type'] == 'specific_date', 'Trigger type mismatch'
    assert rule['date'] == '2024-12-31T10:00:00Z', 'Trigger date mismatch'
    assert rule['condition_type'] == 'balance_threshold', 'Condition type mismatch'
    assert rule['operator'] == 'greater_than', 'Operator mismatch'
    assert rule['amount'] == 500, 'Condition amount mismatch'
    assert rule['action_type'] == 'fixed_transfer', 'Action type mismatch'
    assert rule['action_amount'] == 100, 'Action amount mismatch'
    assert rule['destination_account'] == 'SAV-001', 'Destination account mismatch'

async def test_TC_SCRUM_158_002(page):
    """
    Test Case: TC-SCRUM-158-002
    Steps:
      - Create rule with specific date trigger (current time + 1 min)
      - Balance > $300
      - Transfer $50 action
      - Set account balance
      - Wait for trigger
      - Verify rule evaluation
      - Verify transfer
      - Check execution log
    """
    rule_page = RuleConfigurationPage(page)
    profile_page = ProfilePage(page)
    settings_page = SettingsPage(page)
    # Calculate trigger time
    trigger_time = (datetime.utcnow() + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    await rule_page.navigate_to_rule_creation()
    await rule_page.set_trigger(trigger_type='specific_date', date=trigger_time)
    await rule_page.add_condition(condition_type='balance_threshold', operator='greater_than', amount=300)
    await rule_page.add_action(action_type='fixed_transfer', amount=50, destination_account='SAV-001')
    await rule_page.save_rule()
    # Set account balance
    await profile_page.click_profile()
    await settings_page.open_settings()
    await rule_page.set_account_balance(amount=350)
    # Wait for trigger
    await asyncio.sleep(65)  # Wait for rule to trigger (1 min + buffer)
    # Verify rule evaluation
    rule_eval = await rule_page.get_rule_evaluation()
    assert rule_eval['status'] == 'triggered', 'Rule not triggered as expected'
    # Verify transfer
    transfer = await rule_page.get_transfer()
    assert transfer['amount'] == 50, 'Transfer amount mismatch'
    assert transfer['destination_account'] == 'SAV-001', 'Destination account mismatch'
    # Check execution log
    log = await rule_page.get_execution_log()
    assert log['result'] == 'success', 'Execution log indicates failure'
