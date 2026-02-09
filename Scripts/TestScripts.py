import pytest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration:

    # Existing test methods...

    @pytest.mark.asyncio
    async def test_manual_trigger_minimal_rule(self):
        """TC_SCRUM158_07: Create a rule with only required fields (manual trigger, amount condition == 1, transfer action to account G with amount 1) and verify rule creation."""
        rule_page = RuleConfigurationPage()
        await rule_page.navigate_to_rule_configuration()
        await rule_page.create_rule_manual_trigger_minimal(
            trigger_type='manual',
            amount_condition=1,
            transfer_account='G',
            transfer_amount=1
        )
        success_message = await rule_page.get_success_message()
        assert 'Rule created successfully' in success_message, "Rule creation failed for minimal manual trigger."

    @pytest.mark.asyncio
    async def test_large_metadata_field_rule(self):
        """TC_SCRUM158_08: Create a rule with a large metadata field (manual trigger, metadata string of 10,000 characters) and verify rule creation and performance."""
        rule_page = RuleConfigurationPage()
        await rule_page.navigate_to_rule_configuration()
        large_metadata = 'X' * 10000
        await rule_page.create_rule_with_large_metadata(
            trigger_type='manual',
            metadata=large_metadata
        )
        success_message = await rule_page.get_success_message()
        assert 'Rule created successfully' in success_message, "Rule creation failed for large metadata field."
        # Optionally, add performance assertion if available
        # assert rule_page.last_operation_duration < 5, "Rule creation took too long with large metadata."

    @pytest.mark.asyncio
    async def test_recurring_interval_weekly_rule(self):
        """TC_SCRUM158_03: Create a rule with recurring interval trigger (weekly) and verify scheduling logic."""
        rule_page = RuleConfigurationPage()
        await rule_page.navigate_to_rule_configuration()
        await rule_page.create_recurring_rule(
            trigger_type='recurring',
            interval_value='weekly',
            condition_operator='==',
            condition_value=1,
            action_account='G',
            action_amount=1
        )
        scheduled = await rule_page.submit_rule_and_verify_schedule()
        assert scheduled is True, "Rule was not scheduled for recurring weekly evaluation."

    @pytest.mark.asyncio
    async def test_missing_trigger_field_schema(self):
        """TC_SCRUM158_04: Attempt to create rule with schema missing 'trigger' field and verify error handling."""
        rule_page = RuleConfigurationPage()
        await rule_page.navigate_to_rule_configuration()
        # Example schema missing 'trigger' field
        incomplete_schema = {
            # 'trigger': 'manual',  # intentionally omitted
            'condition': {
                'operator': '==',
                'value': 1
            },
            'action': {
                'account': 'G',
                'amount': 1
            }
        }
        error_message = await rule_page.attempt_create_rule_with_incomplete_schema(incomplete_schema)
        assert 'missing required field' in error_message.lower(), "Schema was not rejected for missing 'trigger' field."
