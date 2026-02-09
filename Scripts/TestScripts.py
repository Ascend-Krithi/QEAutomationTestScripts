# Import necessary modules
from Pages.RuleEnginePage import RuleEnginePage
from Pages.LoginPage import LoginPage
from Pages.RulePage import RulePage
from Pages.TransactionPage import TransactionPage
from Pages.RuleDefinitionPage import RuleDefinitionPage

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
        # ... (rest of original logic)

class TestRuleEngine:
    def __init__(self, driver):
        self.driver = driver
        self.rule_engine = RuleEnginePage(driver)

    def test_specific_date_rule(self):
        rule_json = '{"trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": []}'
        self.rule_engine.enter_rule(rule_json)
        self.rule_engine.submit_rule()
        acceptance = self.rule_engine.wait_for_rule_acceptance()
        assert 'accepted' in acceptance.lower()
        self.rule_engine.simulate_time('2024-07-01T10:00:00Z')
        assert self.rule_engine.verify_transfer_executed(expected_count=1)

    def test_recurring_weekly_rule(self):
        rule_json = '{"trigger": {"type": "recurring", "interval": "weekly"}, "action": {"type": "percentage_of_deposit", "percentage": 10}, "conditions": []}'
        self.rule_engine.enter_rule(rule_json)
        self.rule_engine.submit_rule()
        acceptance = self.rule_engine.wait_for_rule_acceptance()
        assert 'accepted' in acceptance.lower()
        # Simulate several weeks (stub, depends on backend/test hooks)
        for _ in range(4):
            self.rule_engine.simulate_time('weekly')
        assert self.rule_engine.verify_recurring_transfer(interval='weekly', occurrences=4)

# --- New test methods for TC-FT-003 and TC-FT-004 ---
class TestRuleAndTransaction:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RulePage(driver)
        self.transaction_page = TransactionPage(driver)

    def test_define_rule_with_multiple_conditions_and_simulate_deposits(self):
        """
        Test Case TC-FT-003:
        1. Define a rule with multiple conditions (balance >= 1000, source = 'salary').
        2. Simulate deposit from 'salary' when balance is 900 (should NOT execute transfer).
        3. Simulate deposit from 'salary' when balance is 1200 (should execute transfer).
        """
        # Step 1: Define rule
        self.rule_page.define_rule(
            trigger_type='after_deposit',
            action_type='fixed_amount',
            amount=50,
            balance=1000,
            source='salary'
        )
        assert 'accepted' in (self.rule_page.get_success_message() or '').lower()

        # Step 2: Simulate deposit with balance 900 (should not execute transfer)
        self.transaction_page.simulate_deposit(balance=900, deposit=100, source='salary')
        status = self.transaction_page.get_transfer_status()
        assert status is None or 'not executed' in status.lower() or 'no transfer' in status.lower()

        # Step 3: Simulate deposit with balance 1200 (should execute transfer)
        self.transaction_page.simulate_deposit(balance=1200, deposit=100, source='salary')
        status = self.transaction_page.get_transfer_status()
        assert status is not None and ('executed' in status.lower() or 'success' in status.lower())

    def test_submit_rule_with_missing_trigger_type(self):
        """
        Test Case TC-FT-004 Step 1:
        Submit a rule with missing trigger type. Should return error for missing required field.
        """
        self.rule_page.define_rule(
            trigger_type=None,  # Missing trigger
            action_type='fixed_amount',
            amount=100
        )
        error_msg = self.rule_page.get_error_message()
        assert error_msg is not None and ('required' in error_msg.lower() or 'missing' in error_msg.lower())

    def test_submit_rule_with_unsupported_action_type(self):
        """
        Test Case TC-FT-004 Step 2:
        Submit a rule with unsupported action type. Should return error for unsupported action type.
        """
        self.rule_page.define_rule(
            trigger_type='specific_date',
            action_type='unknown_action'
        )
        error_msg = self.rule_page.get_error_message()
        assert error_msg is not None and ('unsupported' in error_msg.lower() or 'invalid' in error_msg.lower())

# --- New test methods for TC-FT-005 and TC-FT-006 ---
class TestRuleDefinitionAndTransaction:
    def __init__(self, driver):
        self.driver = driver
        self.rule_definition_page = RuleDefinitionPage(driver)
        self.transaction_page = TransactionPage(driver)
        self.rule_page = RulePage(driver)

    def test_define_percentage_rule_and_simulate_deposit(self):
        """
        Test Case TC-FT-005:
        1. Define a rule for 10% of deposit action.
        2. Simulate deposit of 500 units.
        3. Verify transfer of 50 units is executed.
        """
        # Step 1: Define percentage rule
        self.rule_definition_page.navigate_to_rule_definition()
        self.rule_definition_page.define_rule(
            trigger={'type': 'after_deposit'},
            action={'type': 'percentage_of_deposit', 'percentage': 10},
            conditions=[]
        )
        self.rule_definition_page.submit_rule()
        assert self.rule_definition_page.is_rule_accepted()

        # Step 2: Simulate deposit
        self.transaction_page.simulate_deposit(balance=0, deposit=500, source='test_source')
        # Step 3: Verify transfer of 50 units
        assert self.transaction_page.verify_percentage_transfer(deposit=500, expected_percentage=10)

    def test_define_future_rule_type_and_verify_existing_rules(self):
        """
        Test Case TC-FT-006:
        1. Define a rule with new future rule type 'currency_conversion'.
        2. Verify system gracefully rejects and existing rules execute as before.
        """
        # Step 1: Define rule with future type
        self.rule_definition_page.navigate_to_rule_definition()
        self.rule_definition_page.define_rule(
            trigger={'type': 'currency_conversion', 'currency': 'EUR'},
            action={'type': 'fixed_amount', 'amount': 100},
            conditions=[]
        )
        self.rule_definition_page.submit_rule()
        error_msg = self.rule_definition_page.handle_unknown_rule_type(
            trigger={'type': 'currency_conversion', 'currency': 'EUR'},
            action={'type': 'fixed_amount', 'amount': 100}
        )
        assert error_msg == "Unknown rule type. Rule not accepted, but existing rules unaffected."

        # Step 2: Verify existing rules still execute
        result = self.rule_page.verify_existing_rules()
        assert result == "Existing rules executed successfully."
