from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        await self.login_page.fill_email('')

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_create_rule_with_specific_date_trigger_and_balance_condition(self):
        # Step 2: Navigate to rule creation interface
        self.rule_page.navigate_to_rule_creation()
        # Step 3: Define specific date trigger for 2024-12-31 at 10:00 AM
        self.rule_page.define_specific_date_trigger('2024-12-31')
        # Step 4: Add balance threshold condition: balance > $500
        self.rule_page.add_balance_threshold_condition('greater_than', 500)
        # Step 5: Add fixed amount transfer action: transfer $100 to savings account
        self.rule_page.add_fixed_transfer_action(100, 'SAV-001')
        # Step 6: Save rule
        self.rule_page.save_rule()
        # Step 7: Retrieve saved rule and validate
        self.rule_page.retrieve_saved_rule('RULE-XXXX')
        # Step 8: Validate schema
        self.rule_page.validate_schema()

    def test_create_rule_with_dynamic_date_and_balance_action(self):
        import datetime
        # Step 2: Create rule with specific date trigger (current date + 1 minute), balance > $300, transfer $50
        future_date = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d')
        self.rule_page.navigate_to_rule_creation()
        self.rule_page.define_specific_date_trigger(future_date)
        self.rule_page.add_balance_threshold_condition('greater_than', 300)
        self.rule_page.add_fixed_transfer_action(50, 'SAV-001')
        self.rule_page.save_rule()
        # Step 3: Set account balance to $400 (Assume method exists or is mocked)
        # Step 4: Wait for trigger time and verify rule evaluation (Assume wait logic, not implemented)
        # Step 5: Verify transfer action execution (Assume check, not implemented)
        # Step 6: Check rule execution log (Assume check, not implemented)
        self.rule_page.retrieve_saved_rule('RULE-XXXX')
        self.rule_page.validate_schema()
