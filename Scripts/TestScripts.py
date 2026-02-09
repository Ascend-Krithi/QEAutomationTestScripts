
import pytest
import asyncio

from Pages.RuleConfigurationPage import RuleConfigurationPage

# Existing tests...

@pytest.mark.asyncio
async def test_TC_SCRUM158_09_create_rule_with_minimum_fields():
    """Test creating a rule with minimum required fields."""
    rule_data = {
        'trigger': 'balance_above',
        'conditions': [{'type': 'amount_above', 'value': 1000}],
        'actions': [{'type': 'transfer', 'amount': 100}]
    }
    rule_page = RuleConfigurationPage()
    response = await rule_page.create_rule_with_minimum_fields(rule_data)
    assert response['success'] is True, f"Expected success, got: {response}"
    assert 'Rule created successfully' in response.get('message', ''), f"Expected success message, got: {response.get('message', '')}"
    assert response.get('schema_valid', False) is True, "Expected JSON schema to be valid."

@pytest.mark.asyncio
async def test_TC_SCRUM158_10_create_rule_with_unsupported_trigger():
    """Test creating a rule with an unsupported trigger type."""
    rule_data = {
        'trigger': 'future_trigger',
        'conditions': [{'type': 'amount_above', 'value': 500}],
        'actions': [{'type': 'transfer', 'amount': 50}]
    }
    rule_page = RuleConfigurationPage()
    response = await rule_page.create_rule_with_unsupported_trigger(rule_data)
    # Accept either error or acceptance message, but must be present
    assert 'message' in response, "API response must contain a message."
    assert response['success'] is False or 'unsupported' in response.get('message', '').lower() or 'accepted' in response.get('message', '').lower(), f"Expected error or acceptance message, got: {response}"