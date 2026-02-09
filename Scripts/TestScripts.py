import pytest
from Pages.LoginPage import LoginPage
from RuleEnginePage import RuleEnginePage
from Pages.RuleCreationPage import RuleCreationPage
from Pages.DepositSimulationPage import DepositSimulationPage
from Pages.RuleValidationPage import RuleValidationPage

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

    async def test_specific_date_rule_trigger(self):
        # TC-FT-001: Define a JSON rule with trigger type 'specific_date' set to a future date
        rule = {
            'trigger': {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'},
            'action': {'type': 'fixed_amount', 'amount': 100},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()
        rule_engine.simulate_time_trigger('2024-07-01T10:00:00Z')
        assert rule_engine.verify_transfer_action(expected_count=1)

    async def test_recurring_weekly_rule_trigger(self):
        # TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly'
        rule = {
            'trigger': {'type': 'recurring', 'interval': 'weekly'},
            'action': {'type': 'percentage_of_deposit', 'percentage': 10},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()
        rule_engine.simulate_recurring_trigger(interval='weekly', times=3)
        assert rule_engine.verify_transfer_action_recurring(expected_intervals=3)

    async def test_rule_with_multiple_conditions(self):
        # TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary')
        rule = {
            'trigger': {'type': 'after_deposit'},
            'action': {'type': 'fixed_amount', 'amount': 50},
            'conditions': [
                {'type': 'balance_threshold', 'operator': '>=', 'value': 1000},
                {'type': 'transaction_source', 'value': 'salary'}
            ]
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()

        # Simulate deposit from 'salary' when balance is 900
        result = rule_engine.simulate_deposit(balance=900, deposit=100, source='salary')
        assert not result['transfer_executed']

        # Simulate deposit from 'salary' when balance is 1200
        result = rule_engine.simulate_deposit(balance=1200, deposit=100, source='salary')
        assert result['transfer_executed']

    async def test_rule_with_missing_trigger_type(self):
        # TC-FT-004: Submit a rule with missing trigger type
        rule = {
            'action': {'type': 'fixed_amount', 'amount': 100},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        response = rule_engine.submit_rule(rule)
        assert response['error'] == 'Missing required field: trigger'

    async def test_rule_with_unsupported_action_type(self):
        # TC-FT-004: Submit a rule with unsupported action type
        rule = {
            'trigger': {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'},
            'action': {'type': 'unknown_action'},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        response = rule_engine.submit_rule(rule)
        assert response['error'] == 'Unsupported action type'

    async def test_deposit_percentage_rule(self):
        # TC-FT-005: Define a rule for 10% of deposit action and simulate deposit of 500 units
        rule_creation_page = RuleCreationPage(self.page)
        deposit_simulation_page = DepositSimulationPage(self.page)
        rule_creation_page.go_to()
        rule_creation_page.select_trigger_type('after_deposit')
        rule_creation_page.select_action_type('percentage_of_deposit')
        rule_creation_page.enter_action_percentage(10)
        rule_creation_page.submit_rule()
        assert rule_creation_page.validate_rule_submission(expected_success=True)
        deposit_simulation_page.go_to()
        deposit_simulation_page.enter_balance(1000)  # Example balance
        deposit_simulation_page.enter_deposit_amount(500)
        deposit_simulation_page.select_source('salary')
        deposit_simulation_page.submit_deposit()
        assert deposit_simulation_page.is_transfer_executed() is True

    async def test_currency_conversion_rule_and_existing_rules(self):
        # TC-FT-006: Define a currency conversion rule, check acceptance/rejection, verify existing rules
        rule_creation_page = RuleCreationPage(self.page)
        rule_validation_page = RuleValidationPage(self.page)
        rule_creation_page.go_to()
        rule_creation_page.select_trigger_type('currency_conversion')
        rule_creation_page.select_action_type('fixed_amount')
        rule_creation_page.enter_action_amount(100)
        rule_creation_page.select_action_currency('EUR')
        rule_creation_page.submit_rule()
        indicator = rule_creation_page.handle_future_rule_type('currency_conversion')
        assert indicator == 'Rule type accepted.' or 'currency_conversion' in indicator
        rule_validation_page.go_to()
        rules = rule_validation_page.get_rule_list()
        for idx, _ in enumerate(rules):
            accepted = rule_validation_page.validate_rule_acceptance(idx)
            rejected = rule_validation_page.validate_rule_rejection(idx)
            assert accepted or rejected
