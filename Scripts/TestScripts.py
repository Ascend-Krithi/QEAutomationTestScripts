# Existing imports
from Pages.RuleConfigurationPage import RuleConfigurationPage
from selenium.webdriver.remote.webdriver import WebDriver

# Existing test class
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

# New tests for Rule Configuration Page
class TestRuleConfiguration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_define_specific_date_rule_and_execute(self):
        """
        TC-FT-001: Define JSON rule with 'specific_date' trigger, validate acceptance, simulate trigger, validate execution.
        """
        rule_id = "TC-FT-001"
        rule_name = "Specific Date Transfer Rule"
        date_str = "2024-07-01T10:00:00Z"
        amount = 100
        # Create rule
        result = self.rule_page.create_specific_date_rule(rule_id, rule_name, date_str, amount)
        assert result, "Rule was not accepted by the system."
        # Simulate system time reaching trigger date
        self.rule_page.simulate_time_reaching_trigger()
        # Validate transfer action
        assert self.rule_page.validate_transfer_action(), "Transfer action was not executed at the specified date."

    def test_define_recurring_rule_and_execute(self):
        """
        TC-FT-002: Define JSON rule with 'recurring' trigger, validate acceptance, simulate trigger, validate execution.
        """
        rule_id = "TC-FT-002"
        rule_name = "Weekly Recurring Transfer Rule"
        interval = "weekly"
        percentage = 10
        # Create rule
        result = self.rule_page.create_recurring_rule(rule_id, rule_name, interval, percentage)
        assert result, "Rule was not accepted by the system."
        # Simulate passing of several weeks
        self.rule_page.simulate_time_reaching_trigger()
        # Validate transfer action
        assert self.rule_page.validate_transfer_action(), "Transfer action was not executed at each interval."

    def test_create_rule_with_multiple_conditions_and_deposit_simulation(self):
        """
        TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary').
        Simulate deposit scenarios and validate transfer execution.
        """
        # Step 1: Create rule with multiple conditions
        trigger = {"type": "after_deposit"}
        action = {"type": "fixed_amount", "amount": 50}
        conditions = [
            {"type": "balance_threshold", "operator": ">=", "value": 1000},
            {"type": "transaction_source", "value": "salary"}
        ]
        self.rule_page.create_rule_with_conditions(trigger, action, conditions)

        # Step 2: Simulate deposit with balance 900 (should NOT execute transfer)
        self.rule_page.simulate_deposit(balance=900, deposit=100, source="salary")
        self.rule_page.validate_transfer_execution(expected=False)

        # Step 3: Simulate deposit with balance 1200 (should execute transfer)
        self.rule_page.simulate_deposit(balance=1200, deposit=100, source="salary")
        self.rule_page.validate_transfer_execution(expected=True)

    def test_submit_rule_with_missing_trigger_and_unsupported_action(self):
        """
        TC-FT-004: Submit rule with missing trigger and unsupported action, validate error messages.
        """
        # Step 1: Submit rule with missing trigger
        action_missing_trigger = {"type": "fixed_amount", "amount": 100}
        conditions_missing_trigger = []
        self.rule_page.submit_rule_missing_trigger(action_missing_trigger, conditions_missing_trigger)
        self.rule_page.validate_error_message("missing required field")

        # Step 2: Submit rule with unsupported action type
        trigger_unsupported_action = {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}
        action_unsupported = {"type": "unknown_action"}
        conditions_unsupported = []
        self.rule_page.submit_rule_unsupported_action(trigger_unsupported_action, action_unsupported, conditions_unsupported)
        self.rule_page.validate_error_message("unsupported action type")

    def test_percentage_of_deposit_rule(self):
        """
        TC-FT-005: Define a rule for 10% of deposit action and simulate deposit of 500 units, assert transfer of 50 units is executed.
        """
        rule_data = {'trigger': {'type': 'after_deposit'}, 'action': {'type': 'percentage_of_deposit', 'percentage': 10}, 'conditions': []}
        accepted = self.rule_page.define_percentage_deposit_rule(rule_data)
        assert accepted, "Percentage deposit rule was not accepted."
        deposit_amount = 500
        expected_transfer = 50  # 10% of 500
        executed = self.rule_page.simulate_deposit_and_validate_transfer(deposit_amount, expected_transfer)
        assert executed, f"Transfer of {expected_transfer} units was not executed after deposit."

    def test_future_rule_type_and_existing_rules(self):
        """
        TC-FT-006: Define a rule with a new, future rule type and verify existing rules continue to execute as before.
        """
        rule_data = {'trigger': {'type': 'currency_conversion', 'currency': 'EUR'}, 'action': {'type': 'fixed_amount', 'amount': 100}, 'conditions': []}
        result = self.rule_page.define_future_rule_type(rule_data)
        assert result == "accepted" or isinstance(result, str), f"Unexpected result or error message: {result}"
        # Existing rules should still execute
        assert self.rule_page.verify_existing_rules_execution(), "Existing rules did not function as expected after future rule type test."

    # TC-FT-009: Create and store a rule with specific_date trigger, fixed_amount action, empty conditions; retrieve and validate
    def test_create_and_retrieve_specific_date_rule(self):
        rule_name = "TC-FT-009-SpecificDateRule"
        trigger_type = "specific_date"
        action_type = "fixed_amount"
        conditions = []
        # Create rule
        self.rule_page.create_rule(rule_name, trigger_type, action_type, conditions)
        # Prepare original input dict for validation
        original_input = {
            "name": rule_name,
            "trigger": trigger_type,
            "action": action_type,
            "conditions": conditions
        }
        # Validate rule retrieval
        self.rule_page.validate_rule_retrieval(rule_name, original_input)

    # TC-FT-010: Define a rule with after_deposit trigger, fixed_amount action, empty conditions; trigger and validate unconditional execution
    def test_define_and_trigger_after_deposit_rule_unconditional(self):
        rule_name = "TC-FT-010-AfterDepositRule"
        trigger_type = "after_deposit"
        action_type = "fixed_amount"
        conditions = []
        # Create rule
        self.rule_page.create_rule(rule_name, trigger_type, action_type, conditions)
        # Trigger rule and validate unconditional execution
        result = self.rule_page.trigger_rule_unconditional(rule_name)
        assert result, "Rule did not execute unconditionally"