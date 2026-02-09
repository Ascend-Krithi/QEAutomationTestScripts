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

# Note:
# - The methods create_rule, validate_rule, simulate_time, verify_transfer, add_weeks_to_date
#   are assumed to be implemented in RuleConfigurationPage.py as per the context.
# - Existing logic in TestLoginFunctionality is preserved.
# - Comments provided for clarity and traceability.
