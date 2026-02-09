# Import necessary modules
from Pages.RuleManagerPage import RuleManagerPage
from selenium.webdriver.remote.webdriver import WebDriver
import pytest
from Pages.RuleEnginePage import RuleEnginePage
from Pages.RulePage import RulePage
from Pages.DepositPage import DepositPage

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

class TestRuleManager:
    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver):
        self.rule_manager = RuleManagerPage(driver)

    def test_specific_date_rule_trigger(self):
        # Test Case TC-FT-001
        self.rule_manager.go_to()
        rule_json = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        self.rule_manager.define_rule(rule_json)
        assert self.rule_manager.is_rule_accepted(), "Rule was not accepted by the system."
        self.rule_manager.simulate_time("2024-07-01T10:00:00Z")
        assert self.rule_manager.is_transfer_executed("SCENARIO-1"), "Transfer action was not executed as expected."

    def test_recurring_weekly_rule_trigger(self):
        # Test Case TC-FT-002
        self.rule_manager.go_to()
        rule_json = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        self.rule_manager.define_rule(rule_json)
        assert self.rule_manager.is_rule_accepted(), "Rule was not accepted by the system."
        # Simulate several weeks
        import datetime
        start_date = datetime.datetime.strptime("2024-07-01T10:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        for i in range(3):
            week_date = (start_date + datetime.timedelta(weeks=i)).isoformat() + "Z"
            self.rule_manager.simulate_time(week_date)
            assert self.rule_manager.is_transfer_executed("SCENARIO-2"), f"Transfer not executed for week {i+1}."

class TestRuleEngine:
    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver):
        self.rule_engine = RuleEnginePage(driver)
        self.deposit_page = DepositPage(driver)

    def test_percentage_of_deposit_rule(self):
        # Test Case TC-FT-005: Define rule for 10% of deposit, simulate deposit of 500
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        self.rule_engine.define_rule(rule_data)
        assert "accepted" in self.rule_engine.get_success_message().lower(), "Rule was not accepted."
        self.rule_engine.simulate_deposit(500)
        # Expect transfer of 50 units
        assert "50" in self.deposit_page.get_transfer_message(), "Transfer of 50 units not executed."

    def test_currency_conversion_rule_and_existing_rules(self):
        # Test Case TC-FT-006: Define new rule with currency_conversion, verify existing rules
        rule_data = {
            "trigger": {"type": "currency_conversion", "currency": "EUR"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        self.rule_engine.define_rule(rule_data)
        success_msg = self.rule_engine.get_success_message()
        error_msg = self.rule_engine.get_error_message()
        assert ("accepted" in success_msg.lower() or "rejected" in error_msg.lower()), "System did not gracefully handle new rule type."
        # Verify existing rules function as expected
        rules = self.rule_engine.list_existing_rules()
        assert len(rules) > 0, "No existing rules found."
        # Simulate deposit for existing rule
        self.rule_engine.simulate_deposit(500)
        assert "transfer" in self.deposit_page.get_transfer_message().lower(), "Existing rules did not execute as expected."
