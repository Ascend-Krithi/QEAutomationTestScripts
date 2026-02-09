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

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_create_specific_date_rule(self):
        """
        Test Case TC-FT-001
        Steps:
        1. Define a JSON rule with trigger type 'specific_date' set to a future date.
        2. Simulate system time reaching the trigger date.
        """
        rule_json = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        validation_message = self.rule_page.create_rule(rule_json)
        assert validation_message == "Rule is accepted by the system."
        self.rule_page.validate_rule_execution("specific_date:2024-07-01T10:00:00Z", expected=True)

    def test_create_recurring_rule(self):
        """
        Test Case TC-FT-002
        Steps:
        1. Define a JSON rule with trigger type 'recurring' and interval 'weekly'.
        2. Simulate passing of several weeks.
        """
        rule_json = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        validation_message = self.rule_page.create_rule(rule_json)
        assert validation_message == "Rule is accepted by the system."
        self.rule_page.validate_rule_execution("recurring:weekly", expected=True)

    def test_create_rule_with_multiple_conditions(self):
        """
        Test Case TC-FT-003
        Steps:
        1. Define a rule with multiple conditions (balance >= 1000, source = 'salary').
        2. Simulate deposit from 'salary' when balance is 900 (expect transfer NOT executed).
        3. Simulate deposit from 'salary' when balance is 1200 (expect transfer executed).
        """
        rule_json = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 50},
            "conditions": [
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        }
        validation_message = self.rule_page.create_rule(rule_json)
        assert validation_message == "Rule is accepted by the system."
        # Simulate deposit with balance 900 (should NOT execute transfer)
        executed = self.rule_page.simulate_deposit(900, 100, "salary")
        assert executed is False
        # Simulate deposit with balance 1200 (should execute transfer)
        executed = self.rule_page.simulate_deposit(1200, 100, "salary")
        assert executed is True

    def test_rule_with_missing_trigger(self):
        """
        Test Case TC-FT-004
        Steps:
        1. Submit rule with missing trigger type (expect error for missing field).
        2. Submit rule with unsupported action type (expect error for unsupported action).
        """
        # Step 1: Missing trigger type
        rule_json_missing_trigger = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        error_message = self.rule_page.submit_invalid_rule(rule_json_missing_trigger)
        assert "missing required field" in error_message.lower()
        # Step 2: Unsupported action type
        rule_json_unsupported_action = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        error_message = self.rule_page.submit_invalid_rule(rule_json_unsupported_action)
        assert "unsupported action type" in error_message.lower()
