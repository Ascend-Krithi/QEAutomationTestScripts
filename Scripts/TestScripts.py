# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
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
        self.driver = driver
        self.rule_management_page = RuleManagementPage(driver)

    def test_specific_date_rule(self):
        self.rule_management_page.go_to_rule_management()
        rule_data = '{"trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": []}'
        self.rule_management_page.define_specific_date_rule(rule_data)
        assert self.rule_management_page.is_rule_accepted(), "Rule was not accepted by the system."
        self.rule_management_page.simulate_system_time("2024-07-01T10:00:00Z")
        assert self.rule_management_page.is_transfer_executed(), "Transfer action was not executed at the specified date."

    def test_recurring_rule(self):
        self.rule_management_page.go_to_rule_management()
        rule_data = '{"trigger": {"type": "recurring", "interval": "weekly"}, "action": {"type": "percentage_of_deposit", "percentage": 10}, "conditions": []}'
        self.rule_management_page.define_recurring_rule(rule_data)
        assert self.rule_management_page.is_rule_accepted(), "Rule was not accepted by the system."
        self.rule_management_page.simulate_weeks(3)
        assert self.rule_management_page.is_recurring_transfer_executed(), "Recurring transfer action was not executed as expected."