
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

class TestRuleManagement:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleManagementPage(driver)

    async def test_create_rule_multiple_conditions_TC_FT_003(self):
        # Step 1: Define a rule with multiple conditions (balance >= 1000, source = 'salary')
        await self.rule_page.navigate_to_rule_management()
        rule_data = {
            'name': 'Salary Transfer Rule',
            'trigger_type': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000},
                {'field': 'source', 'operator': '=', 'value': 'salary'}
            ],
            'action_type': 'transfer',
            'action_params': {'amount': 500}
        }
        await self.rule_page.create_new_rule(rule_data)
        await self.rule_page.submit_rule()

        # Step 2: Simulate a deposit from 'salary' when balance is 900; expect transfer NOT executed
        await self.rule_page.simulate_deposit(source='salary', amount=900)
        transfer_executed = await self.rule_page.check_transfer_executed()
        assert not transfer_executed, 'Transfer should NOT be executed when balance < 1000'

        # Step 3: Simulate a deposit from 'salary' when balance is 1200; expect transfer executed
        await self.rule_page.simulate_deposit(source='salary', amount=1200)
        transfer_executed = await self.rule_page.check_transfer_executed()
        assert transfer_executed, 'Transfer should be executed when balance >= 1000 and source is salary'

    async def test_submit_rule_missing_invalid_fields_TC_FT_004(self):
        await self.rule_page.navigate_to_rule_management()
        # Step 1: Submit a rule with missing trigger type; expect error for missing required field
        rule_data_missing_trigger = {
            'name': 'Missing Trigger Rule',
            'trigger_type': '',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action_type': 'transfer',
            'action_params': {'amount': 100}
        }
        await self.rule_page.create_new_rule(rule_data_missing_trigger)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert 'trigger type is required' in error_msg.lower(), 'Expected error for missing trigger type'

        # Step 2: Submit a rule with unsupported action type; expect error for unsupported action type
        rule_data_invalid_action = {
            'name': 'Invalid Action Rule',
            'trigger_type': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action_type': 'unsupported_action',
            'action_params': {'amount': 100}
        }
        await self.rule_page.create_new_rule(rule_data_invalid_action)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert 'unsupported action type' in error_msg.lower(), 'Expected error for unsupported action type'