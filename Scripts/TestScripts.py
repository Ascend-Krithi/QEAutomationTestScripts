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
        """
        TC-FT-001:
        - Create a rule with specific_date: 2024-07-01T10:00:00Z, amount: 100
        - Verify rule acceptance
        - Simulate date
        - Verify transfer executed once
        """
        # Step 1: Create rule
        rule_details = {
            'rule_type': 'specific_date',
            'date': '2024-07-01T10:00:00Z',
            'amount': 100
        }
        self.rule_page.create_rule(rule_details)
        # Step 2: Validate rule acceptance
        self.assertTrue(self.rule_page.validate_rule(rule_details), "Rule acceptance failed")
        # Step 3: Simulate date
        self.rule_page.simulate_time('2024-07-01T10:00:00Z')
        # Step 4: Verify transfer executed once
        transfer_count = self.rule_page.verify_transfer(rule_details)
        self.assertEqual(transfer_count, 1, "Transfer was not executed exactly once")

    def test_recurring_weekly_rule_acceptance_and_transfer(self):
        """
        TC-FT-002:
        - Create recurring rule (interval weekly, percentage 10)
        - Verify rule acceptance
        - Simulate weeks
        - Verify transfer at each interval
        """
        # Step 1: Create recurring rule
        rule_details = {
            'rule_type': 'recurring',
            'interval': 'weekly',
            'percentage': 10
        }
        self.rule_page.create_rule(rule_details)
        # Step 2: Validate rule acceptance
        self.assertTrue(self.rule_page.validate_rule(rule_details), "Recurring rule acceptance failed")
        # Step 3: Simulate multiple weeks
        start_date = '2024-07-01T10:00:00Z'
        weeks_to_simulate = 4
        for week in range(weeks_to_simulate):
            simulated_date = self.rule_page.add_weeks_to_date(start_date, week)
            self.rule_page.simulate_time(simulated_date)
            # Step 4: Verify transfer at each interval
            transfer_count = self.rule_page.verify_transfer(rule_details, date=simulated_date)
            self.assertEqual(transfer_count, 1, f"Transfer not executed for week {week+1} ({simulated_date})")

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
        # Step 1: Define rule with multiple conditions
        self.rule_page.define_multi_condition_rule(rule_id, rule_name, 1000, 'salary')
        # Step 2: Validate rule acceptance
        self.assertTrue(self.rule_page.is_rule_accepted(), "Rule was not accepted.")
        # Step 3: Simulate deposit with balance 900 (should NOT execute transfer)
        result = self.rule_page.simulate_deposit_and_validate_transfer(900, expect_transfer=False)
        self.assertTrue(result, "Transfer should NOT be executed when balance is 900.")
        # Step 4: Simulate deposit with balance 1200 (should execute transfer)
        result = self.rule_page.simulate_deposit_and_validate_transfer(1200, expect_transfer=True)
        self.assertTrue(result, "Transfer should be executed when balance is 1200.")

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
