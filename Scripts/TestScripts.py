
import unittest
from selenium import webdriver
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.page = RuleConfigurationPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test methods...

    def test_TC_FT_007_performance_load_and_evaluate_rules(self):
        """TC-FT-007: Performance - Load 10,000 rules and evaluate all"""
        # Step 1: Load 10,000 rules
        rules = self._generate_rules(10000)
        self.page.load_batch_rules(rules)
        # Step 2: Evaluate all rules
        self.page.evaluate_all_rules()
        # Step 3: Validate performance (e.g., ensure operation completes within acceptable time)
        performance_ok = self.page.validate_performance(expected_rule_count=10000, max_seconds=60)
        self.assertTrue(performance_ok, "Performance validation failed: Loading and evaluation exceeded threshold.")

    def test_TC_FT_008_security_sql_injection_rejection(self):
        """TC-FT-008: Security - Submit rule with SQL injection and verify rejection"""
        # Step 1: Submit rule with SQL injection payload
        sql_injection_payload = "DROP TABLE rules;--"
        result = self.page.submit_rule_with_sql_injection(sql_injection_payload)
        # Step 2: Verify system rejects the rule
        self.assertTrue(result['rejected'], "SQL injection rule was not rejected as expected.")
        self.assertIn("SQL injection detected", result['message'], "Expected SQL injection rejection message not found.")

    def _generate_rules(self, count):
        """Utility to generate dummy rules for batch loading"""
        return [
            {
                'name': f'Rule_{i}',
                'condition': f'IF value > {i} THEN action_{i}',
                'action': f'action_{i}'
            }
            for i in range(count)
        ]
