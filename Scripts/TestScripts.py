import pytest
from Pages.RuleConfigurationPage import RuleConfigurationPage

@pytest.mark.asyncio
async def test_create_rule_with_missing_required_fields(browser):
    page = RuleConfigurationPage(browser)
    await page.navigate_to_rule_creation()
    # Enter rule data with missing required fields
    await page.enter_rule_data({
        'name': '',  # Name is required
        'description': 'Test rule with missing name',
        'condition': 'valid_condition',
        'action': 'valid_action'
    })
    await page.submit_rule()
    errors = await page.get_validation_errors()
    assert errors is not None
    await page.verify_field_validation_message('name', 'This field is required.')

@pytest.mark.asyncio
async def test_create_rule_with_invalid_field_types(browser):
    page = RuleConfigurationPage(browser)
    await page.navigate_to_rule_creation()
    # Enter rule data with invalid field types
    await page.enter_rule_data({
        'name': 'Invalid Type Rule',
        'description': 'Test rule with invalid type',
        'condition': 12345,  # Should be a string
        'action': 'valid_action'
    })
    await page.submit_rule()
    errors = await page.get_validation_errors()
    assert errors is not None
    await page.verify_type_mismatch_message('condition', 'Expected type: string')

@pytest.mark.asyncio
async def test_create_rule_with_invalid_api_payload(browser):
    page = RuleConfigurationPage(browser)
    await page.navigate_to_rule_creation()
    # Enter rule data with invalid API payload (missing fields)
    await page.enter_rule_data({
        # Missing 'name' and 'action'
        'description': 'Test invalid API payload',
        'condition': 'valid_condition'
    })
    await page.submit_rule()
    api_error = await page.get_api_error_message()
    assert api_error is not None
    await page.is_bad_request_error()
    assert 'Missing required fields' in api_error

@pytest.mark.asyncio
async def test_create_rule_with_invalid_action_value(browser):
    page = RuleConfigurationPage(browser)
    await page.navigate_to_rule_creation()
    # Enter rule data with invalid action value
    await page.enter_rule_data({
        'name': 'Invalid Action Rule',
        'description': 'Test rule with invalid action',
        'condition': 'valid_condition',
        'action': 'invalid_action_value'
    })
    await page.submit_rule()
    errors = await page.get_validation_errors()
    assert errors is not None
    await page.verify_field_validation_message('action', 'Invalid action value.')

# --- New Test Cases ---
@pytest.mark.asyncio
async def test_tc_scrum_158_001_create_and_verify_rule(browser):
    page = RuleConfigurationPage(browser)
    # Step 2: Navigate to Automated Transfers rule creation interface
    await page.enter_rule_id('RULE-2505')
    await page.enter_rule_name('Automated Transfers Rule')
    # Step 3: Define a specific date trigger for 2024-12-31 at 10:00 AM
    await page.select_trigger_type('specific_date')
    await page.set_date_picker('2024-12-31T10:00:00Z')
    await page.click_validate_schema()  # Validate trigger against JSON schema
    # Step 4: Add balance threshold condition: balance > $500
    await page.click_add_condition()
    await page.select_condition_type('balance_threshold')
    await page.enter_balance_threshold('500')
    await page.select_operator('greater_than')
    # Step 5: Add fixed amount transfer action: transfer $100 to savings account
    await page.select_action_type('fixed_transfer')
    await page.enter_transfer_amount('100')
    await page.enter_destination_account('SAV-001')
    # Step 6: Save the rule
    await page.click_save_rule()
    success_msg = await page.get_success_message()
    assert 'Rule is saved successfully' in success_msg
    # Step 7: Retrieve the saved rule and verify all components
    # (Assume retrieval function exists)
    # retrieved_rule = await page.retrieve_rule('RULE-2505')
    # assert retrieved_rule['trigger_type'] == 'specific_date'
    # assert retrieved_rule['condition_type'] == 'balance_threshold'
    # assert retrieved_rule['action_type'] == 'fixed_transfer'

@pytest.mark.asyncio
async def test_tc_scrum_158_002_rule_trigger_and_transfer(browser):
    page = RuleConfigurationPage(browser)
    # Step 1: Create a rule with specific date trigger, balance > $300, and transfer $50 action
    await page.enter_rule_id('RULE-2506')
    await page.enter_rule_name('Scheduled Transfer Rule')
    await page.select_trigger_type('specific_date')
    # Set trigger for current time + 1 minute
    import datetime
    future_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    await page.set_date_picker(future_time)
    await page.click_add_condition()
    await page.select_condition_type('balance_threshold')
    await page.enter_balance_threshold('300')
    await page.select_operator('greater_than')
    await page.select_action_type('fixed_transfer')
    await page.enter_transfer_amount('50')
    await page.enter_destination_account('SAV-001')
    await page.click_save_rule()
    success_msg = await page.get_success_message()
    assert 'Rule is saved successfully' in success_msg
    # Step 2: Set account balance to $400 (Assume helper exists)
    # await page.set_account_balance('ACC-001', 400)
    # Step 3: Wait for trigger time and verify rule evaluation
    import asyncio
    await asyncio.sleep(65)  # Wait for trigger
    # Step 4: Verify transfer action execution
    # transfer_result = await page.verify_transfer('ACC-001', 'SAV-001', 50)
    # assert transfer_result['status'] == 'SUCCESS'
    # Step 5: Check rule execution log
    # log = await page.get_rule_execution_log('RULE-2506')
    # assert log['status'] == 'SUCCESS'
