# Existing imports and test methods preserved
from selenium import webdriver
import unittest
from Pages.RuleManagementPage import RuleManagementPage

class TestRuleManagement(unittest.TestCase):
    # ... Existing test methods ...

    def test_TC_FT_003_rule_creation_and_transfer_validation(self):
        ...
    def test_TC_FT_004_rule_submission_missing_trigger_and_unsupported_action(self):
        ...

    def test_TC_FT_005_percentage_of_deposit_rule(self):
        """
        TC-FT-005:
        Step 1: Define a rule for 10% of deposit action.
        Step 2: Simulate deposit of 500 units, expect transfer of 50 units.
        """
        driver = webdriver.Chrome()
        page = RuleManagementPage(driver)
        try:
            # Step 1: Create a rule for 10% of deposit
            page.create_percentage_of_deposit_rule(10)

            # Step 2: Simulate deposit of 500 units, expect transfer of 50 units
            deposit_amount = 500
            expected_transfer = 50
            page.simulate_and_validate_percentage_transfer(deposit_amount, expected_transfer)
        finally:
            driver.quit()

    def test_TC_FT_006_currency_conversion_rule_and_existing_rules_execution(self):
        """
        TC-FT-006:
        Step 1: Define a rule with trigger type 'currency_conversion', fixed amount 100 EUR. System must accept or gracefully reject.
        Step 2: Verify existing rules continue to execute as before.
        """
        driver = webdriver.Chrome()
        page = RuleManagementPage(driver)
        try:
            # Step 1: Create currency conversion rule
            page.create_currency_conversion_rule('EUR', 100)
            # Validate graceful rejection or acceptance
            page.validate_graceful_rejection()

            # Step 2: Validate existing rules execution
            page.validate_existing_rules_execution()
        finally:
            driver.quit()

    def test_TC_FT_007_batch_rule_loading_and_performance(self):
        """
        TC-FT-007:
        Step 1: Load 10,000 valid rules into the system.
        Step 2: Trigger evaluation for all rules simultaneously.
        """
        driver = webdriver.Chrome()
        page = RuleManagementPage(driver)
        try:
            # Step 1: Generate and load 10,000 valid rules
            rules = [
                {
                    'conditions': {'cond_key': f'value{i}'},
                    'actions': {'action_key': f'action{i}'}
                }
                for i in range(10000)
            ]
            page.load_rules_batch(rules)

            # Step 2: Trigger evaluation and measure performance
            elapsed = page.trigger_evaluation_and_measure_performance(timeout_threshold=60)
            assert elapsed <= 60, f"Batch evaluation exceeded performance threshold: {elapsed:.2f}s"
        finally:
            driver.quit()

    def test_TC_FT_008_sql_injection_rule_submission_and_rejection(self):
        """
        TC-FT-008:
        Step 1: Submit a rule with SQL injection in a field value.
        """
        driver = webdriver.Chrome()
        page = RuleManagementPage(driver)
        try:
            page.submit_rule_with_sql_injection_and_validate_rejection()
        finally:
            driver.quit()
