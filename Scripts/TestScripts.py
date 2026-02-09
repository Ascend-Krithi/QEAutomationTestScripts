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

    def test_TC_FT_009_create_and_validate_specific_date_rule(self):
        """TC-FT-009: Create and store a valid rule with trigger type 'specific_date', then retrieve and validate"""
        rule_id = "tcft009_rule"
        rule_name = "TCFT009_SpecificDateRule"
        date_str = "2024-07-01T10:00:00Z"
        amount = 100
        # Step 1: Create and store the rule
        self.page.create_and_store_specific_date_rule(rule_id, rule_name, date_str, amount)
        # Step 2: Retrieve and validate
        expected_rule_data = {
            "rule_id": rule_id,
            "rule_name": rule_name,
            "trigger_type": "specific_date",
            "trigger_date": date_str,
            "action_type": "fixed_amount",
            "amount": amount
        }
        valid = self.page.retrieve_rule_and_validate(rule_id, expected_rule_data)
        self.assertTrue(valid, f"Rule retrieved does not match expected data: {expected_rule_data}")

    def test_TC_FT_010_after_deposit_fixed_amount_rule_unconditional_transfer(self):
        """TC-FT-010: Define a rule with 'after_deposit', trigger it with deposit, and verify unconditional transfer"""
        rule_id = "tcft010_rule"
        rule_name = "TCFT010_AfterDepositRule"
        amount = 100
        deposit_amount = 1000
        expected_transfer_amount = 100
        # Step 1: Create the rule (empty conditions)
        self.page.create_after_deposit_fixed_amount_rule(rule_id, rule_name, amount)
        # Step 2: Trigger rule and verify transfer
        transfer_valid = self.page.trigger_rule_and_verify_transfer(deposit_amount, expected_transfer_amount)
        self.assertTrue(transfer_valid, f"Transfer not executed as expected for deposit {deposit_amount} and amount {expected_transfer_amount}")

    def test_TC_SCRUM158_03_create_and_schedule_recurring_interval_rule(self):
        """TC_SCRUM158_03: Create a schema with a recurring interval trigger (weekly) and verify scheduling logic."""
        rule_name = "SCRUM158_03_WeeklyIntervalRule"
        interval_type = "Weekly"
        interval_value = "1"
        trigger_value = "weekly"
        result = self.page.create_recurring_interval_rule(rule_name, interval_type, interval_value, trigger_value)
        self.assertTrue(result, "Rule was not accepted and scheduled for recurring evaluation.")

    def test_TC_SCRUM158_04_validate_missing_trigger_error(self):
        """TC_SCRUM158_04: Submit schema missing 'trigger' field and verify error message."""
        rule_schema = {
            "conditions": [{"type": "amount", "operator": "<", "value": 50}],
            "actions": [{"type": "transfer", "account": "D", "amount": 50}]
        }
        result = self.page.validate_missing_trigger_error(rule_schema)
        self.assertTrue(result, "Schema was not rejected with error indicating missing required 'trigger' field.")

    def test_TC_SCRUM158_07_create_rule_with_required_fields(self):
        """TC_SCRUM158_07: Prepare a schema with only required fields (one trigger, one condition, one action). Submit the schema and verify rule creation."""
        rule_id = "scrum15807_rule"
        rule_name = "SCRUM15807_RequiredFieldsRule"
        condition_type = "amount"
        operator = "=="
        value = 1
        action_type = "transfer"
        account = "G"
        amount = 1
        result = self.page.create_rule_with_required_fields(rule_id, rule_name, condition_type, operator, value, action_type, account, amount)
        self.assertTrue(result, "Rule was not accepted and created as expected.")

    def test_TC_SCRUM158_08_submit_schema_with_large_metadata(self):
        """TC_SCRUM158_08: Prepare a schema with a large metadata field (e.g., 10,000 characters). Submit and verify acceptance/performance."""
        rule_id = "scrum15808_rule"
        rule_name = "SCRUM15808_LargeMetadataRule"
        metadata = "A" * 10000  # Large metadata string
        result = self.page.submit_schema_with_large_metadata(rule_id, rule_name, metadata)
        self.assertTrue(result, "Rule was not accepted or performance was not acceptable.")

    def test_TC_SCRUM158_09_malicious_script_metadata(self):
        """TC_SCRUM158_09: Prepare a schema with metadata containing a malicious script. Submit and verify error response."""
        error_msg = self.page.test_malicious_script_metadata()
        self.assertIsNotNone(error_msg, "Rule was not rejected for malicious script.")
        self.assertTrue("invalid" in error_msg.lower() or "error" in error_msg.lower(), "Error does not indicate invalid content.")

    def test_TC_SCRUM158_10_unsupported_trigger_type(self):
        """TC_SCRUM158_10: Prepare a schema with unsupported trigger type. Submit and verify error or warning response."""
        error_msg = self.page.test_unsupported_trigger_type()
        self.assertIsNotNone(error_msg, "Rule was not rejected for unsupported trigger type.")
        self.assertTrue("unsupported" in error_msg.lower() or "extensibility" in error_msg.lower() or "error" in error_msg.lower(), "Error does not indicate extensibility issue.")
