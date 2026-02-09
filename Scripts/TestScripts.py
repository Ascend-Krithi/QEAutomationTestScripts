import unittest
from RuleEnginePage import RuleEnginePage
import time

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.rule_engine = RuleEnginePage()

    # Existing test methods...
    # (Preserved - do not modify existing code below unless specified)

    def test_TC_FT_007_load_and_evaluate_bulk_rules(self):
        """TC-FT-007: Load 10,000 rules and evaluate all, asserting acceptable performance."""
        num_rules = 10000
        rules = [{"id": f"rule_{i}", "definition": f"IF x > {i} THEN y = {i*2}"} for i in range(num_rules)]
        start_load = time.time()
        self.rule_engine.load_bulk_rules(rules)
        end_load = time.time()
        load_duration = end_load - start_load

        self.assertTrue(load_duration < 30, f"Loading 10,000 rules took too long: {load_duration:.2f}s")

        start_eval = time.time()
        eval_result = self.rule_engine.trigger_evaluation_all_rules()
        end_eval = time.time()
        eval_duration = end_eval - start_eval

        self.assertTrue(eval_duration < 60, f"Evaluating 10,000 rules took too long: {eval_duration:.2f}s")
        self.assertIsInstance(eval_result, dict, "Evaluation result should be a dictionary.")

    def test_TC_FT_008_submit_rule_with_sql_injection(self):
        """TC-FT-008: Submit a rule with SQL injection and assert system rejects it."""
        sql_injection_rule = {
            "id": "sql_injection_rule",
            "definition": "1; DROP TABLE users; --"
        }
        response = self.rule_engine.submit_rule_with_sql_injection(sql_injection_rule)
        # Assume response has 'accepted' boolean and 'error' string
        self.assertFalse(response.get("accepted", True), "System should reject SQL injection rule.")
        self.assertIn("SQL injection", response.get("error", ""), "Error message should indicate SQL injection detected.")

if __name__ == "__main__":
    unittest.main()
