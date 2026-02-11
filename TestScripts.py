import pytest
from selenium.webdriver.common.by import By
from PageClasses import LoginPage, RuleConfigurationPage

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
        await self.login_page.fill_email('')
        # ... (previous logic continues)

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_TC_SCRUM158_001_create_and_validate_rule(self):
        """
        TC_SCRUM158_001: Create a new rule with specific trigger, condition, and action, validate schema, simulate deposit, and ensure rule is stored.
        """
        await self.rule_page.navigate_to_rule_configuration()
        await self.rule_page.click_create_new_rule()
        await self.rule_page.set_trigger('Deposit Received')
        await self.rule_page.set_condition('Amount > 1000')
        await self.rule_page.set_action('Send Notification')
        await self.rule_page.enter_json_schema({
            "type": "object",
            "properties": {
                "amount": {"type": "number"},
                "currency": {"type": "string"}
            },
            "required": ["amount", "currency"]
        })
        assert await self.rule_page.validate_json_schema() == True
        await self.rule_page.simulate_deposit(amount=1500, currency="USD")
        assert await self.rule_page.check_rule_applied('Send Notification') == True
        assert await self.rule_page.rule_exists_in_storage('Deposit Received', 'Amount > 1000', 'Send Notification') == True

    async def test_TC_SCRUM158_002_invalid_schema_and_rule_storage(self):
        """
        TC_SCRUM158_002: Attempt to create a rule with invalid schema, check validation failure, and verify rule is not stored.
        """
        await self.rule_page.navigate_to_rule_configuration()
        await self.rule_page.click_create_new_rule()
        await self.rule_page.set_trigger('Deposit Received')
        await self.rule_page.set_condition('Amount < 100')
        await self.rule_page.set_action('Block Deposit')
        await self.rule_page.enter_json_schema({
            "type": "object",
            "properties": {
                "amount": {"type": "number"}
                # Missing required 'currency' property intentionally
            },
            "required": ["amount", "currency"]
        })
        assert await self.rule_page.validate_json_schema() == False
        await self.rule_page.simulate_deposit(amount=50, currency="USD")
        assert await self.rule_page.check_rule_applied('Block Deposit') == False
        assert await self.rule_page.rule_exists_in_storage('Deposit Received', 'Amount < 100', 'Block Deposit') == False
