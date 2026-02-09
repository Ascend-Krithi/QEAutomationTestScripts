import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

class TestRuleCreationAndScheduling:
    def __init__(self, driver):
        self.driver = driver
        self.rule_creation_page = RuleCreationPage(driver)
        self.rule_scheduling_page = RuleSchedulingPage(driver)

    def test_specific_date_rule(self):
        # TC-FT-001: Specific Date Rule
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        self.rule_creation_page.open_rule_creation()
        self.rule_creation_page.enter_rule_json(rule_data)
        self.rule_creation_page.submit_rule()
        assert self.rule_creation_page.verify_rule_accepted() is True, "Rule was not accepted by the system."
        self.rule_scheduling_page.simulate_time()
        assert self.rule_scheduling_page.verify_transfer_executed() is True, "Transfer action was not executed at the specified date."

    def test_recurring_weekly_rule(self):
        # TC-FT-002: Recurring Weekly Rule
        rule_data = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        self.rule_creation_page.open_rule_creation()
        self.rule_creation_page.enter_rule_json(rule_data)
        self.rule_creation_page.submit_rule()
        assert self.rule_creation_page.verify_rule_accepted() is True, "Rule was not accepted by the system."
        for _ in range(3):  # Simulate three weeks
            self.rule_scheduling_page.simulate_time()
            assert self.rule_scheduling_page.verify_transfer_executed() is True, "Transfer action was not executed at the interval."
        history = self.rule_scheduling_page.get_transfer_history()
        assert history.count('Transfer executed') >= 3, "Transfer action was not executed at the start of each interval."

# TC-FT-003: Define rule with multiple conditions (balance >= 1000, source = 'salary'), simulate deposits, verify transfer
class TestMultipleConditionsRule:
    def __init__(self, page):
        self.profile_page = ProfilePage(page)

    async def test_define_rule_and_simulate_deposit(self):
        # Define rule with multiple conditions
        await self.profile_page.define_rule(
            trigger_type='after_deposit',
            action_type='fixed_amount',
            amount=50,
            conditions=[
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        )
        # Simulate deposit with balance 900, deposit 100, source 'salary'
        await self.profile_page.simulate_deposit(balance=900, deposit=100, source='salary')
        await self.profile_page.verify_transfer_execution(expected_result=False)
        # Simulate deposit with balance 1200, deposit 100, source 'salary'
        await self.profile_page.simulate_deposit(balance=1200, deposit=100, source='salary')
        await self.profile_page.verify_transfer_execution(expected_result=True)

# TC-FT-004: Submit rule with missing trigger and unsupported action, verify error
class TestRuleSubmissionErrors:
    def __init__(self, page):
        self.settings_page = SettingsPage(page)

    async def test_missing_trigger_type(self):
        # Submit a rule with missing trigger type
        rule_data = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        await self.settings_page.submit_rule(rule_data)
        await self.settings_page.verify_error_message("missing required field")

    async def test_unsupported_action_type(self):
        # Submit a rule with unsupported action type
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        await self.settings_page.submit_rule(rule_data)
        await self.settings_page.verify_error_message("unsupported action type")
