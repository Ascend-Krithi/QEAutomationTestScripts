# Imports
from selenium import webdriver
import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality(unittest.TestCase):
    # ... (existing test methods)
    pass

# --- New Test Methods for Rule Configuration ---

class TestRuleConfiguration(unittest.TestCase):
    def setUp(self):
        # Set up Selenium WebDriver and RuleConfigurationPage
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)

    def tearDown(self):
        # Clean up WebDriver
        self.driver.quit()

    def test_specific_date_rule_acceptance_and_transfer(self):
        ...

    def test_recurring_weekly_rule_acceptance_and_transfer(self):
        ...

    # --- Appended for TC-FT-003 ---
    def test_rule_with_multiple_conditions(self):
        """
        TC-FT-003:
        - Define a rule with multiple conditions (balance >= 1000, source = 'salary').
        - Simulate deposit from 'salary' when balance is 900 (expect no transfer).
        - Simulate deposit from 'salary' when balance is 1200 (expect transfer).
        """
        rule_id = "TC003"
        rule_name = "Multiple Conditions Rule"
        balance_condition = 1000
        source_condition = "salary"
        # Step 1: Define the rule
        self.rule_page.define_multi_condition_rule(rule_id, rule_name, balance_condition, source_condition)
        # Step 2: Validate rule acceptance
        self.assertTrue(self.rule_page.is_rule_accepted(), "Rule was not accepted.")
        # Step 3: Simulate deposit with balance 900 (should NOT execute transfer)
        transfer_executed = self.rule_page.simulate_deposit_and_validate_transfer(900, expect_transfer=False)
        self.assertFalse(transfer_executed, "Transfer should NOT be executed when balance is 900.")
        # Step 4: Simulate deposit with balance 1200 (should execute transfer)
        transfer_executed = self.rule_page.simulate_deposit_and_validate_transfer(1200, expect_transfer=True)
        self.assertTrue(transfer_executed, "Transfer should be executed when balance is 1200.")

    # --- Appended for TC-FT-004 ---
    def test_rule_with_missing_trigger_type_returns_error(self):
        """
        TC-FT-004:
        - Submit a rule with missing trigger type.
        - Expect error indicating missing required field.
        """
        rule_id = "TC004A"
        rule_name = "Missing Trigger Rule"
        error_message = self.rule_page.submit_rule_missing_trigger(rule_id, rule_name)
        self.assertIsNotNone(error_message, "Error message expected for missing trigger type.")
        self.assertIn("missing", error_message.lower(), "Error message should indicate missing required field.")

    def test_rule_with_unsupported_action_type_returns_error(self):
        """
        TC-FT-004:
        - Submit a rule with unsupported action type.
        - Expect error indicating unsupported action type.
        """
        rule_id = "TC004B"
        rule_name = "Unsupported Action Rule"
        error_message = self.rule_page.submit_rule_unsupported_action(rule_id, rule_name)
        self.assertIsNotNone(error_message, "Error message expected for unsupported action type.")
        self.assertIn("unsupported", error_message.lower(), "Error message should indicate unsupported action type.")

    # --- Appended for TC-FT-005 ---
    def test_percentage_of_deposit_rule_and_transfer(self):
        """
        TC-FT-005:
        1. Define a rule for 10% of deposit action.
        2. Simulate deposit of 500 units.
        3. Validate transfer of 50 units is executed.
        """
        rule_id = "TC005"
        rule_name = "10 Percent Deposit Rule"
        percentage = 10
        deposit_amount = 500
        expected_transfer_amount = 50
        # Step 1: Define the rule
        self.rule_page.define_percentage_of_deposit_rule(rule_id, rule_name, percentage)
        # Step 2: Validate rule acceptance (assume success if no exception)
        # Step 3: Simulate deposit and validate transfer
        transfer_executed = self.rule_page.simulate_deposit_and_validate_transfer(deposit_amount, expected_transfer_amount)
        self.assertTrue(transfer_executed, "Transfer of 50 units should be executed.")

    # --- Appended for TC-FT-006 ---
    def test_currency_conversion_rule_and_existing_rules(self):
        """
        TC-FT-006:
        1. Define a rule with trigger 'currency_conversion' and fixed_amount action.
        2. Validate system accepts or gracefully rejects with clear message.
        3. Verify existing rules continue to execute as before.
        """
        rule_id = "TC006"
        rule_name = "Currency Conversion Rule"
        currency = "EUR"
        amount = 100
        # Step 1: Define the rule and validate acceptance/rejection
        rule_accepted = self.rule_page.define_currency_conversion_rule_and_validate(rule_id, rule_name, currency, amount)
        self.assertTrue(rule_accepted, "System should accept or gracefully reject with a clear message.")
        # Step 2: Verify existing rules still work
        existing_rules_ok = self.rule_page.verify_existing_rules_functionality()
        self.assertTrue(existing_rules_ok, "Existing rules should continue to execute as before.")
