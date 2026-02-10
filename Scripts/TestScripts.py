
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
