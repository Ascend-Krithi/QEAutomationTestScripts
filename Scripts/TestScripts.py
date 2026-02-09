
import pytest
import asyncio
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration:

    @pytest.mark.asyncio
    async def test_TC_SCRUM158_01(self, browser):
        # Existing test implementation
        pass

    @pytest.mark.asyncio
    async def test_TC_SCRUM158_02(self, browser):
        # Existing test implementation
        pass

    # --- New test cases appended below ---

    @pytest.mark.asyncio
    async def test_TC_SCRUM158_03(self, browser):
        '''
        TC_SCRUM158_03:
        - Create a schema with a recurring interval trigger (weekly), condition amount >= 1000, action transfer 1000 to account C.
        - Submit the rule and verify that it is scheduled for weekly execution (assert success message).
        '''
        rule_page = RuleConfigurationPage(browser)
        await rule_page.navigate_to_rule_configuration()

        # Fill in schema fields
        await rule_page.set_rule_name('Weekly Transfer Rule')
        await rule_page.set_trigger_type('Recurring')
        await rule_page.set_trigger_interval('Weekly')
        await rule_page.set_condition_field('amount')
        await rule_page.set_condition_operator('>=')
        await rule_page.set_condition_value('1000')
        await rule_page.set_action_type('Transfer')
        await rule_page.set_action_amount('1000')
        await rule_page.set_action_account('C')

        # Submit rule
        await rule_page.submit_rule()

        # Assert scheduled for weekly execution (success message)
        success_message = await rule_page.get_success_message()
        assert 'scheduled for weekly execution' in success_message.lower()
        assert 'rule created successfully' in success_message.lower()

    @pytest.mark.asyncio
    async def test_TC_SCRUM158_04(self, browser):
        '''
        TC_SCRUM158_04:
        - Prepare a schema missing the 'trigger' field (condition amount < 50, action transfer 50 to account D).
        - Attempt to create the rule and verify that the schema is rejected with an error indicating the missing required field (assert error message).
        '''
        rule_page = RuleConfigurationPage(browser)
        await rule_page.navigate_to_rule_configuration()

        # Fill in schema fields, omit trigger
        await rule_page.set_rule_name('Missing Trigger Rule')
        # trigger intentionally not set
        await rule_page.set_condition_field('amount')
        await rule_page.set_condition_operator('<')
        await rule_page.set_condition_value('50')
        await rule_page.set_action_type('Transfer')
        await rule_page.set_action_amount('50')
        await rule_page.set_action_account('D')

        # Submit rule
        await rule_page.submit_rule()

        # Assert error for missing required field
        error_message = await rule_page.get_error_message()
        assert 'missing required field' in error_message.lower()
        assert 'trigger' in error_message.lower()