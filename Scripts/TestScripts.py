from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.RuleManagementPage import RuleManagementPage

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
        self.rule_page = RuleManagementPage(driver)

    def test_TC_FT_003(self):
        # Step 2: Define a rule with multiple conditions
        conditions = {'balance': '>=1000', 'source': 'salary'}
        actions = {'transfer': 'execute'}
        self.rule_page.create_rule(conditions, actions)
        # Expected: Rule is accepted
        # Step 3: Simulate deposit from 'salary' when balance is 900
        self.rule_page.simulate_deposit(900, 'salary')
        # Expected: Transfer is NOT executed
        self.rule_page.validate_transfer_execution(False)
        # Step 4: Simulate deposit from 'salary' when balance is 1200
        self.rule_page.simulate_deposit(1200, 'salary')
        # Expected: Transfer is executed
        self.rule_page.validate_transfer_execution(True)

    def test_TC_FT_004(self):
        # Step 2: Submit a rule with missing trigger type
        self.rule_page.submit_rule_with_invalid_data(None, 'fixed_amount')
        self.rule_page.validate_error_messages(['missing required field'])
        # Step 3: Submit a rule with unsupported action type
        self.rule_page.submit_rule_with_invalid_data('specific_date', 'unknown_action')
        self.rule_page.validate_error_messages(['unsupported action type'])
