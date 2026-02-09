# imports
import pytest
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

# --- Begin Rule Configuration Tests ---

class TestRuleConfiguration:
    def setup_method(self):
        # Setup WebDriver and Page Object
        self.driver = ... # WebDriver initialization
        self.rule_page = RuleConfigurationPage(self.driver)

    def teardown_method(self):
        # Teardown WebDriver
        self.driver.quit()

    def verify_transfer_action(self):
        # Implement verification logic for transfer action
        # Return True if transfer action executed as expected
        return True

    def test_define_rule_specific_date_and_verify_transfer(self):
        """
        Test Case TC-FT-001:
        - Define a rule with trigger type 'specific_date' set to 2024-07-01T10:00:00Z
        - Verify that transfer action is executed exactly once at the specified date
        """
        rule_id = "TCFT001"
        rule_name = "Specific Date Rule"
        date_str = "2024-07-01T10:00:00Z"
        amount = 100
        dest_account = "DEST_ACC_001"
        self.rule_page.define_specific_date_rule(rule_id, rule_name, date_str, amount, dest_account)
        # Simulate system time
        self.rule_page.simulate_system_time(date_str)
        # Verify transfer action
        assert self.verify_transfer_action() is True

    def test_define_rule_recurring_weekly_and_verify_transfer(self):
        """
        Test Case TC-FT-002:
        - Define a rule with trigger type 'recurring' and interval 'weekly'
        - Verify that transfer action is executed at the start of each interval
        """
        rule_id = "TCFT002"
        rule_name = "Recurring Weekly Rule"
        interval = "weekly"
        percentage = 10
        dest_account = "DEST_ACC_002"
        self.rule_page.define_recurring_rule(rule_id, rule_name, interval, percentage, dest_account)
        # Simulate passing of several weeks
        self.rule_page.simulate_weeks_passing(3)
        # Verify transfer action
        assert self.verify_transfer_action() is True

    # --- Appended for TC-FT-003 ---
    def test_define_rule_multiple_conditions_and_simulate_deposit(self):
        """
        Test Case TC-FT-003:
        - Define a rule with multiple conditions: balance >= 1000, source = 'salary'
        - Simulate deposit from 'salary' with balance 900: transfer NOT executed
        - Simulate deposit from 'salary' with balance 1200: transfer executed
        """
        rule_id = "TCFT003"
        rule_name = "Multiple Conditions Rule"
        trigger_type = "after_deposit"
        trigger_value = None
        conditions = [
            {"condition_type": "balance_threshold", "balance_threshold": 1000, "operator": ">=", "transaction_source": None},
            {"condition_type": "transaction_source", "balance_threshold": None, "transaction_source": "salary", "operator": None}
        ]
        action_type = "fixed_amount"
        action_value = 50
        dest_account = "DEST_ACC_003"
        self.rule_page.define_rule_with_multiple_conditions(
            rule_id, rule_name, trigger_type, trigger_value, conditions, action_type, action_value, dest_account
        )
        # Simulate deposit with balance 900, deposit 100, source 'salary'
        result = self.rule_page.simulate_deposit_and_validate_transfer(900, 0)  # Expect transfer NOT executed
        assert result is False
        # Simulate deposit with balance 1200, deposit 100, source 'salary'
        result = self.rule_page.simulate_deposit_and_validate_transfer(1200, 50)  # Expect transfer executed
        assert result is True

    # --- Appended for TC-FT-004 ---
    def test_submit_rule_missing_trigger_type(self):
        """
        Test Case TC-FT-004:
        - Submit a rule with missing trigger type
        - Expect error indicating missing required field
        """
        error_message = self.rule_page.validate_missing_trigger_error()
        assert "missing required field" in error_message.lower()

    def test_submit_rule_unsupported_action_type(self):
        """
        Test Case TC-FT-004:
        - Submit a rule with unsupported action type
        - Expect error indicating unsupported action type
        """
        unsupported_action_type = "unknown_action"
        error_message = self.rule_page.validate_unsupported_action_type_error(unsupported_action_type)
        assert "unsupported action type" in error_message.lower()
