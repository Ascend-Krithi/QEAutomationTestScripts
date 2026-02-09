
import unittest
import time
from RuleEnginePage import RuleEnginePage

class TestRuleEngine(unittest.TestCase):

    # Existing test methods...

    def test_load_10000_rules_and_evaluate_performance_TC_FT_007(self):
        """TC-FT-007: Load 10,000 valid rules and trigger evaluation, measuring performance."""
        rule_engine = RuleEnginePage()
        # Generate 10,000 valid rules (as dictionaries)
        rules = []
        for i in range(10000):
            rules.append({
                'rule_id': f'R{i}',
                'name': f'Rule {i}',
                'condition': f'value > {i}',
                'action': 'approve'
            })
        # Load bulk rules
        start_load = time.time()
        load_result = rule_engine.load_bulk_rules(rules)
        end_load = time.time()
        self.assertTrue(load_result['success'], f"Bulk load failed: {load_result.get('error')}")
        load_duration = end_load - start_load
        print(f"Bulk load of 10,000 rules took {load_duration:.2f} seconds.")
        # Evaluate all rules
        start_eval = time.time()
        eval_result = rule_engine.evaluate_all_rules()
        end_eval = time.time()
        self.assertTrue(eval_result['success'], f"Evaluation failed: {eval_result.get('error')}")
        eval_duration = end_eval - start_eval
        print(f"Evaluation of 10,000 rules took {eval_duration:.2f} seconds.")
        # Acceptance criteria: durations should meet performance thresholds (example: < 60 seconds)
        self.assertLess(load_duration, 60, "Bulk load exceeded performance threshold.")
        self.assertLess(eval_duration, 60, "Evaluation exceeded performance threshold.")

    def test_sql_injection_rule_rejection_TC_FT_008(self):
        """TC-FT-008: Submit a rule with SQL injection and verify rejection."""
        rule_engine = RuleEnginePage()
        # Rule with SQL injection attempt in 'condition'
        malicious_rule = {
            'rule_id': 'SQL_INJ_1',
            'name': 'Malicious Rule',
            'condition': "1; DROP TABLE users;--",
            'action': 'approve'
        }
        submit_result = rule_engine.submit_rule(malicious_rule)
        # Expecting rejection
        self.assertFalse(submit_result['success'], "System accepted a rule with SQL injection.")
        self.assertIn('rejected', submit_result.get('message', '').lower(), "No rejection message for SQL injection.")
        self.assertNotIn('executed', submit_result.get('message', '').lower(), "SQL was executed when it should not have been.")
        print(f"SQL injection test result: {submit_result.get('message', '')}")

if __name__ == '__main__':
    unittest.main()
