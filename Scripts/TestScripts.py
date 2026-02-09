# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.RuleEnginePage import RuleEnginePage
import pytest

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.go_to()
        self.login_page.enter_email('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        assert self.login_page.is_empty_field_prompt_visible()

    def test_remember_me_functionality(self):
        self.login_page.go_to()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('password123')
        self.login_page.set_remember_me(True)
        self.login_page.click_login()
        assert self.login_page.is_dashboard_header_visible()

    def test_tc_ft_001_specific_date_trigger(self):
        rule = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        pass  # Placeholder for actual implementation

    def test_tc_ft_002_recurring_weekly_trigger(self):
        rule = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        pass  # Placeholder for actual implementation

class TestRuleEngine:
    def __init__(self, driver):
        self.driver = driver
        self.rule_engine_page = RuleEnginePage(driver)

    def test_tc_ft_003_multiple_conditions_deposit_simulation(self):
        # Step 2: Define rule with multiple conditions
        rule = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 50},
            "conditions": [
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        }
        self.rule_engine_page.define_rule(rule["trigger"], rule["action"], rule["conditions"])
        result = self.rule_engine_page.get_rule_submission_result()
        assert result is not None and "accepted" in result.lower()

        # Step 3: Simulate deposit from 'salary' when balance is 900
        self.rule_engine_page.simulate_deposit(900, 100, "salary")
        transfer_result = self.rule_engine_page.get_transfer_execution_result()
        assert transfer_result is not None and "not executed" in transfer_result.lower()

        # Step 4: Simulate deposit from 'salary' when balance is 1200
        self.rule_engine_page.simulate_deposit(1200, 100, "salary")
        transfer_result = self.rule_engine_page.get_transfer_execution_result()
        assert transfer_result is not None and "executed" in transfer_result.lower()

    def test_tc_ft_004_rule_submission_errors(self):
        # Step 2: Submit a rule with missing trigger type
        rule_missing_trigger = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        self.rule_engine_page.define_rule(rule_missing_trigger.get("trigger", {}), rule_missing_trigger["action"], rule_missing_trigger["conditions"])
        error_message = self.rule_engine_page.get_error_message()
        assert error_message is not None and "missing required field" in error_message.lower()

        # Step 3: Submit a rule with unsupported action type
        rule_unsupported_action = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        self.rule_engine_page.define_rule(rule_unsupported_action["trigger"], rule_unsupported_action["action"], rule_unsupported_action["conditions"])
        error_message = self.rule_engine_page.get_error_message()
        assert error_message is not None and "unsupported action type" in error_message.lower()
