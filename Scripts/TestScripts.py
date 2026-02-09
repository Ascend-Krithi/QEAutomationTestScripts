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

    # TC-FT-003: Multi-condition rule definition and validation
    def test_multi_condition_rule_definition_and_validation(self):
        # Step 1: Define rule with conditions (balance >= 1000, source = 'salary')
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 50},
            "conditions": [
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        }
        self.rule_engine.define_rule_with_conditions(rule_data)
        assert "accepted" in self.rule_engine.get_success_message().lower(), "Rule was not accepted."
        # Step 2: Simulate deposit from 'salary' when balance is 900
        self.rule_engine.simulate_deposit_with_source(balance=900, deposit=100, source="salary")
        assert self.rule_engine.validate_transfer_not_executed(), "Transfer should NOT be executed for balance < 1000."
        # Step 3: Simulate deposit from 'salary' when balance is 1200
        self.rule_engine.simulate_deposit_with_source(balance=1200, deposit=100, source="salary")
        assert self.rule_engine.validate_transfer_executed(), "Transfer should be executed for balance >= 1000."

    # TC-FT-004: Rule submission error handling
    def test_rule_submission_error_handling(self):
        # Step 1: Submit rule with missing trigger type
        rule_data_missing_trigger = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        error_msg = self.rule_engine.submit_rule_missing_trigger(rule_data_missing_trigger)
        assert "missing required field" in error_msg.lower(), "System did not return error for missing trigger type."
        # Step 2: Submit rule with unsupported action type
        rule_data_unsupported_action = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        error_msg = self.rule_engine.submit_rule_unsupported_action(rule_data_unsupported_action)
        assert "unsupported action type" in error_msg.lower(), "System did not return error for unsupported action type."

@pytest.mark.performance
def test_batch_load_and_evaluate_rules(rule_engine_page, perf_threshold_seconds=30):
    """
    TC-FT-007: Load 10,000 valid rules in batch and trigger evaluation for all rules.
    Assert upload and evaluation complete within performance threshold.
    """
    import time

    # Generate 10,000 dummy rules
    rules = [
        {"rule_id": f"R{i}", "condition": f"value > {i}", "action": "accept"}
        for i in range(10000)
    ]
    start_time = time.time()
    upload_result = rule_engine_page.batch_load_rules(rules)
    assert upload_result, "Batch rule upload failed."
    eval_result = rule_engine_page.evaluate_all_rules()
    assert eval_result, "Batch rule evaluation failed."
    elapsed = time.time() - start_time
    assert elapsed < perf_threshold_seconds, f"Batch operation exceeded performance threshold: {elapsed:.2f}s"

@pytest.mark.security
def test_sql_injection_rejection(rule_page):
    """
    TC-FT-008: Submit a rule with SQL injection in a field value.
    Assert that the system rejects the rule and no SQL is executed.
    """
    # Example SQL injection payload
    malicious_rule = {
        "rule_id": "R_SQLI",
        "condition": "'; DROP TABLE rules; --",
        "action": "accept"
    }
    rule_page.submit_rule_with_sql_injection(malicious_rule)
    rejected = rule_page.is_rule_rejected(malicious_rule)
    assert rejected, "Rule with SQL injection was not rejected as expected."