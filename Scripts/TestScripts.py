import pytest
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('...')
        # Add further steps as needed

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_TC_FT_001_create_rule(self):
        # TC-FT-001: Verify that a new rule can be created successfully
        await self.rule_page.navigate_to_rule_configuration()
        await self.rule_page.click_create_rule_button()
        await self.rule_page.fill_rule_name("Sample Rule")
        await self.rule_page.set_rule_conditions({"condition_type": "Amount", "value": "100"})
        await self.rule_page.save_rule()
        assert await self.rule_page.is_rule_created("Sample Rule") is True

    async def test_TC_FT_002_edit_rule(self):
        # TC-FT-002: Verify that an existing rule can be edited successfully
        await self.rule_page.navigate_to_rule_configuration()
        await self.rule_page.search_rule("Sample Rule")
        await self.rule_page.open_rule_for_edit("Sample Rule")
        await self.rule_page.edit_rule_name("Sample Rule Updated")
        await self.rule_page.update_rule_conditions({"condition_type": "Amount", "value": "200"})
        await self.rule_page.save_rule()
        assert await self.rule_page.is_rule_updated("Sample Rule Updated") is True

    async def test_TC_FT_003_define_rule_and_simulate_deposit(self):
        # TC-FT-003: Define a rule with multiple conditions, simulate deposits, and validate transfer
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 50},
            "conditions": [
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        }
        await self.rule_page.define_rule_with_conditions(rule_data)
        success = await self.rule_page.validate_system_response('success')
        assert success is not None, 'Rule creation should be successful.'
        # Simulate deposit with balance 900 (should NOT execute transfer)
        await self.rule_page.simulate_deposit(900, 100, 'salary')
        notransfer = await self.rule_page.validate_system_response('error')
        assert notransfer is not None, 'Transfer should NOT be executed.'
        # Simulate deposit with balance 1200 (should execute transfer)
        await self.rule_page.simulate_deposit(1200, 100, 'salary')
        transfer = await self.rule_page.validate_system_response('success')
        assert transfer is not None, 'Transfer should be executed.'

    async def test_TC_FT_004_submit_rule_missing_trigger(self):
        # TC-FT-004: Submit a rule with missing trigger type, expect error
        rule_data = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        error = await self.rule_page.submit_rule_with_missing_fields(rule_data)
        assert error is not None, "System should return error for missing trigger type."

    async def test_TC_FT_004_submit_rule_unsupported_action(self):
        # TC-FT-004: Submit a rule with unsupported action type, expect error
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        error = await self.rule_page.submit_rule_with_unsupported_action(rule_data)
        assert error is not None, "System should return error for unsupported action type."
