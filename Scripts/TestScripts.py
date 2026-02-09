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
