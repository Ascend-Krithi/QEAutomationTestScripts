import pytest
import asyncio
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration:
    # Existing async test methods...
    
    @pytest.mark.asyncio
    async def test_TC_SCRUM158_05_create_rule_with_invalid_trigger(self):
        rule_id = 'InvalidTriggerRule01'
        rule_name = 'InvalidTriggerRule'
        schema_text = '{"triggers": [{"type": "unknown_trigger"}], "conditions": [{"type": "balanceThreshold", "value": 1000}], "actions": [{"type": "transfer", "amount": 500}]}'
        page = RuleConfigurationPage()
        result = await page.create_rule_with_invalid_trigger(rule_id, rule_name, schema_text)
        assert result['status'] == 'error', f"Expected error status for invalid trigger, got: {result['status']}"
        assert 'invalid trigger' in result['message'].lower(), f"Expected error message about invalid trigger, got: {result['message']}"

    @pytest.mark.asyncio
    async def test_TC_SCRUM158_06_create_rule_with_missing_condition_params(self):
        rule_id = 'MissingCondParamsRule01'
        rule_name = 'MissingCondParamsRule'
        schema_text = '{"triggers": [{"type": "onDeposit"}], "conditions": [{"type": "amount_above"}], "actions": [{"type": "transfer", "amount": 500}]}'
        page = RuleConfigurationPage()
        result = await page.create_rule_with_missing_condition_params(rule_id, rule_name, schema_text)
        assert result['status'] == 'error', f"Expected error status for missing condition parameters, got: {result['status']}"
        assert 'missing' in result['message'].lower(), f"Expected error message about missing condition parameters, got: {result['message']}"
