import pytest
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage
import datetime
import asyncio

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
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_create_specific_date_fixed_amount_rule(self):
        """
        TC-FT-001: Create a rule with trigger type 'specific_date' (date: 2024-07-01T10:00:00Z),
        action 'fixed_amount' (amount: 100), conditions: [].
        Validate rule acceptance and that the transfer action is executed exactly once at the specified date.
        """
        await self.rule_page.navigate()
        rule_name = f"SpecificDateFixedAmount_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        trigger_type = "specific_date"
        trigger_details = {"date": "2024-07-01T10:00:00Z"}
        action_type = "fixed_amount"
        action_details = {"amount": 100}
        conditions = []

        await self.rule_page.create_rule(
            name=rule_name,
            trigger_type=trigger_type,
            trigger_details=trigger_details,
            action_type=action_type,
            action_details=action_details,
            conditions=conditions
        )

        # Validate rule acceptance
        assert await self.rule_page.is_rule_accepted(rule_name), "Rule should be accepted"

        # Simulate waiting for the specified date and validate execution
        # (Assume RuleConfigurationPage provides a method to check execution status)
        await self.rule_page.wait_until_date(trigger_details["date"])
        execution_count = await self.rule_page.get_rule_execution_count(rule_name)
        assert execution_count == 1, f"Rule should execute exactly once, got {execution_count}"

    async def test_create_weekly_percentage_of_deposit_rule(self):
        """
        TC-FT-002: Create a rule with trigger type 'recurring' (interval: weekly),
        action 'percentage_of_deposit' (percentage: 10), conditions: [].
        Validate rule acceptance and that the transfer action is executed at the start of each interval.
        """
        await self.rule_page.navigate()
        rule_name = f"WeeklyPercentageDeposit_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        trigger_type = "recurring"
        trigger_details = {"interval": "weekly"}
        action_type = "percentage_of_deposit"
        action_details = {"percentage": 10}
        conditions = []

        await self.rule_page.create_rule(
            name=rule_name,
            trigger_type=trigger_type,
            trigger_details=trigger_details,
            action_type=action_type,
            action_details=action_details,
            conditions=conditions
        )

        # Validate rule acceptance
        assert await self.rule_page.is_rule_accepted(rule_name), "Rule should be accepted"

        # Simulate checking execution at the start of each interval (weekly)
        # Assume we can check for at least two executions to verify recurrence
        executions = await self.rule_page.get_rule_executions_within_interval(rule_name, interval="weekly")
        assert len(executions) >= 2, f"Rule should execute at least twice for weekly interval, got {len(executions)}"

    async def test_create_rule_with_multiple_conditions(self):
        """
        TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary').
        Simulate deposit scenarios and validate transfer execution.
        """
        await self.rule_page.navigate()
        rule_name = f"MultipleConditions_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        trigger_type = "after_deposit"
        trigger_details = {}
        action_type = "fixed_amount"
        action_details = {"amount": 50}
        conditions = [
            {"type": "balance_threshold", "operator": ">=", "threshold": 1000},
            {"type": "transaction_source", "operator": None, "source": "salary"}
        ]

        await self.rule_page.create_rule(
            rule_id=rule_name,
            rule_name=rule_name,
            trigger_type=trigger_type,
            trigger_data=trigger_details,
            action_type=action_type,
            action_data=action_details,
            conditions=conditions,
            destination_account=None
        )
        # Assert rule accepted
        self.rule_page.assert_rule_accepted()

        # Simulate deposit with balance=900, deposit=100, source='salary'
        self.rule_page.simulate_deposit(balance=900, deposit=100, source="salary")
        self.rule_page.assert_transfer_not_executed()

        # Simulate deposit with balance=1200, deposit=100, source='salary'
        self.rule_page.simulate_deposit(balance=1200, deposit=100, source="salary")
        self.rule_page.assert_transfer_executed()

    async def test_rule_with_missing_trigger_type(self):
        """
        TC-FT-004: Submit a rule with missing trigger type and validate error.
        """
        await self.rule_page.navigate()
        rule_name = f"MissingTrigger_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        trigger_type = None
        trigger_details = {}
        action_type = "fixed_amount"
        action_details = {"amount": 100}
        conditions = []

        await self.rule_page.create_rule(
            rule_id=rule_name,
            rule_name=rule_name,
            trigger_type=trigger_type,
            trigger_data=trigger_details,
            action_type=action_type,
            action_data=action_details,
            conditions=conditions,
            destination_account=None
        )
        self.rule_page.assert_missing_required_field_error()

    async def test_rule_with_unsupported_action_type(self):
        """
        TC-FT-004: Submit a rule with unsupported action type and validate error.
        """
        await self.rule_page.navigate()
        rule_name = f"UnsupportedAction_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        trigger_type = "specific_date"
        trigger_details = {"date": "2024-07-01T10:00:00Z"}
        action_type = "unknown_action"
        action_details = {}
        conditions = []

        await self.rule_page.create_rule(
            rule_id=rule_name,
            rule_name=rule_name,
            trigger_type=trigger_type,
            trigger_data=trigger_details,
            action_type=action_type,
            action_data=action_details,
            conditions=conditions,
            destination_account=None
        )
        self.rule_page.assert_unsupported_action_type_error()
