import pytest
import asyncio
import time
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration:
    """
    Test suite for Rule Configuration Page functionality.
    """

    # ... [existing test methods here] ...

    async def test_batch_rule_loading_and_evaluation_performance(self):
        """
        TC-FT-007: Batch rule loading and evaluation performance.
        Acceptance Criteria:
            - Loading 10,000 valid rules via load_rules_batch(rules_json) completes in <60 seconds.
            - Evaluating all rules via trigger_evaluate_all_rules() completes in <120 seconds.
        """
        rule_page = RuleConfigurationPage()
        
        # Generate dummy batch of 10,000 valid rules
        dummy_rule = {
            "trigger": {"type": "event", "event": "login"},
            "action": {"type": "notification", "message": "Welcome"},
            "conditions": [{"type": "user_status", "value": "active"}]
        }
        rules_json = [dummy_rule for _ in range(10000)]

        # Step 1: Load rules batch and assert performance
        start_time = time.time()
        await rule_page.load_rules_batch(rules_json)
        load_time = time.time() - start_time
        assert load_time < 60, f"Batch loading exceeded threshold: {load_time:.2f}s"

        # Step 2: Evaluate all rules and assert performance
        start_eval = time.time()
        await rule_page.trigger_evaluate_all_rules()
        eval_time = time.time() - start_eval
        assert eval_time < 120, f"Evaluation exceeded threshold: {eval_time:.2f}s"

    async def test_sql_injection_in_rule_submission(self):
        """
        TC-FT-008: SQL injection rejection in rule submission.
        Acceptance Criteria:
            - Submitting a rule with SQL injection payload in conditions is rejected.
            - Error message is returned and rule is not accepted.
        """
        rule_page = RuleConfigurationPage()
        sql_injection_rule = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": [{"type": "balance_threshold", "value": "1000; DROP TABLE users;--"}]
        }

        result = await rule_page.submit_rule_with_sql_injection(sql_injection_rule)
        assert result is not None, "No response returned for SQL injection submission"
        assert "error" in result, "Error message not returned for SQL injection"
        assert result["error"], "System did not reject SQL injection rule"
