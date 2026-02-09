import unittest
from RuleEnginePage import RuleEnginePage
from DepositPage import DepositPage
from RulePage import RulePage

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.rule_engine = RuleEnginePage()
        self.deposit_page = DepositPage()
        self.rule_page = RulePage()

    # ... [existing methods remain unchanged] ...

    def test_TC_FT_009_create_and_store_specific_date_rule(self):
        """TC-FT-009: Create and store rule with trigger 'specific_date', action 'fixed_amount', amount 100, no conditions. Retrieve and assert details match."""
        rule_input = {
            'trigger': {
                'type': 'specific_date',
                'date': '2024-07-01T10:00:00Z'
            },
            'action': {
                'type': 'fixed_amount',
                'amount': 100
            },
            'conditions': []
        }
        rule_id = self.rule_engine.create_and_store_rule(rule_input)
        retrieved_rule = self.rule_engine.retrieve_rule(rule_id)
        self.assertEqual(retrieved_rule['trigger']['type'], 'specific_date')
        self.assertEqual(retrieved_rule['trigger']['date'], '2024-07-01T10:00:00Z')
        self.assertEqual(retrieved_rule['action']['type'], 'fixed_amount')
        self.assertEqual(retrieved_rule['action']['amount'], 100)
        self.assertEqual(retrieved_rule['conditions'], [])

    def test_TC_FT_010_after_deposit_fixed_amount_transfer(self):
        """TC-FT-010: Define rule with trigger 'after_deposit', action 'fixed_amount', amount 100, no conditions. Trigger with deposit=1000 and assert transfer is executed unconditionally."""
        rule_input = {
            'trigger': {
                'type': 'after_deposit'
            },
            'action': {
                'type': 'fixed_amount',
                'amount': 100
            },
            'conditions': []
        }
        rule_id = self.rule_engine.create_and_store_rule(rule_input)
        execution_result = self.rule_engine.execute_rule(rule_id, {'deposit': 1000})
        self.assertTrue(execution_result['executed'])
        self.assertEqual(execution_result['transfer_amount'], 100)
        self.assertEqual(execution_result['conditions_met'], True)

    def test_TC_FT_007_batch_load_and_evaluate_rules(self):
        """TC-FT-007: Batch load 10,000 valid rules and evaluate them using RuleEnginePage. Assert load and evaluation within performance thresholds."""
        import time
        # Generate 10,000 rules
        rules = []
        for i in range(10000):
            rule = {
                'trigger': {'type': 'after_deposit'},
                'action': {'type': 'fixed_amount', 'amount': 10 + (i % 100)},
                'conditions': []
            }
            rules.append(rule)
        start_time = time.time()
        self.rule_engine.batch_load_rules(rules)
        eval_start = time.time()
        evaluation_results = self.rule_engine.evaluate_all_rules()
        eval_end = time.time()
        total_time = eval_end - start_time
        eval_time = eval_end - eval_start
        # Assert all rules are processed
        self.assertEqual(len(evaluation_results), 10000)
        # Performance threshold: load + eval < 10 seconds, eval < 5 seconds
        self.assertLess(total_time, 10, "Batch load & eval exceeded 10s")
        self.assertLess(eval_time, 5, "Evaluation exceeded 5s")

    def test_TC_FT_008_sql_injection_rule_rejection(self):
        """TC-FT-008: Submit rule with SQL injection via RulePage and assert rejection and no SQL execution."""
        # Rule with SQL injection in trigger value
        rule_data = {
            'trigger': {
                'type': "after_deposit",
                'value': "1000; DROP TABLE rules;"
            },
            'action': {
                'type': 'fixed_amount',
                'amount': 100
            },
            'conditions': []
        }
        self.rule_page.submit_rule_with_sql_injection(rule_data)
        rejected = self.rule_page.is_rule_rejected()
        self.assertTrue(rejected, "Rule with SQL injection should be rejected.")
