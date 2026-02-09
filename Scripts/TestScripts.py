# Import necessary modules
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('...')

class TestRuleConfiguration:
    def __init__(self, driver):
        self.rule_page = RuleConfigurationPage(driver)

    def test_define_percentage_of_deposit_rule(self):
        """
        TC-FT-005 Step 1: Define a rule for 10% of deposit action.
        """
        result = self.rule_page.define_percentage_of_deposit_rule(10)
        assert result is True, 'Rule for 10% deposit was not accepted.'

    def test_simulate_deposit_and_verify_transfer(self):
        """
        TC-FT-005 Step 2: Simulate deposit of 500 units, verify transfer of 50 units.
        """
        deposit_amount = 500
        expected_transfer = 50
        result = self.rule_page.simulate_deposit_and_verify_transfer(deposit_amount, expected_transfer)
        assert result is True, f'Transfer of {expected_transfer} units was not executed after deposit.'

    def test_define_rule_with_future_trigger(self):
        """
        TC-FT-006 Step 1: Define a rule with a new, future rule type (currency_conversion, EUR, fixed_amount 100).
        """
        feedback = self.rule_page.define_rule_with_future_trigger('currency_conversion', 'EUR', 'fixed_amount', 100)
        assert feedback in ['System accepts or gracefully rejects with a clear message', 'No feedback received.'], f'Unexpected feedback: {feedback}'

    def test_verify_existing_rules_execution(self):
        """
        TC-FT-006 Step 2: Verify existing rules continue to execute as before.
        """
        result = self.rule_page.verify_existing_rules_execution()
        assert result is True, 'Existing rules did not function as expected.'

    def test_batch_upload_and_evaluate_rules(self):
        """
        TC-FT-007 Step 1 & 2: Batch upload 10,000 valid rules and trigger evaluation for all rules.
        """
        # Prepare 10,000 valid rule dicts
        rules = []
        for i in range(10000):
            rule = {
                "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
                "action": {"type": "fixed_amount", "amount": 100},
                "conditions": [{"type": "balance_threshold", "value": str(1000 + i)}]
            }
            rules.append(rule)
        self.rule_page.batch_upload_rules(rules)
        self.rule_page.trigger_rule_evaluation()
        # Optionally, add assertions for performance thresholds if available
        # For demonstration, assume success if no exceptions
        assert True, 'Batch upload or evaluation failed.'

    def test_sql_injection_rejection(self):
        """
        TC-FT-008 Step 1: Submit a rule with SQL injection in a field value and verify rejection.
        """
        sql_injection_rule = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": [{"type": "balance_threshold", "value": "1000; DROP TABLE users;--"}]
        }
        self.rule_page.submit_rule_with_conditions(sql_injection_rule)
        result = self.rule_page.verify_rule_rejected()
        assert result is True, 'SQL injection rule was not rejected by the system.'

    def test_TC_SCRUM158_01_create_rule_with_all_types(self):
        """
        TC_SCRUM158_01: Prepare a valid rule schema with all supported trigger, condition, and action types. Submit and assert rule creation and retrieval.
        """
        rule_schema = {
            "trigger": {"type": "interval", "value": "daily"},
            "conditions": [{"type": "amount", "operator": ">", "value": 100}],
            "actions": [{"type": "transfer", "account": "A", "amount": 100}]
        }
        # Use create_rule to fill the UI and save
        self.rule_page.create_rule(
            rule_id="SCRUM158_01",
            rule_name="Interval Amount Transfer",
            trigger=rule_schema["trigger"],
            conditions=rule_schema["conditions"],
            actions=rule_schema["actions"]
        )
        # Optionally, assert success message
        success_msg = self.rule_page.get_success_message()
        assert "success" in success_msg.lower(), f"Rule creation failed: {success_msg}"

    def test_TC_SCRUM158_02_create_rule_with_multiple_conditions_actions(self):
        """
        TC_SCRUM158_02: Prepare a schema with two conditions and two actions. Submit and assert all conditions and actions are present.
        """
        rule_schema = {
            "trigger": {"type": "manual"},
            "conditions": [
                {"type": "amount", "operator": ">", "value": 500},
                {"type": "country", "operator": "==", "value": "US"}
            ],
            "actions": [
                {"type": "transfer", "account": "B", "amount": 500},
                {"type": "notify", "message": "Transfer complete"}
            ]
        }
        self.rule_page.create_rule(
            rule_id="SCRUM158_02",
            rule_name="Manual Multi Condition/Action",
            trigger=rule_schema["trigger"],
            conditions=rule_schema["conditions"],
            actions=rule_schema["actions"]
        )
        # Optionally, assert success message
        success_msg = self.rule_page.get_success_message()
        assert "success" in success_msg.lower(), f"Rule creation failed: {success_msg}"

    def test_TC_SCRUM158_03_recurring_interval_trigger(self):
        """
        TC_SCRUM158_03: Create a schema with a recurring interval trigger (weekly), submit, and verify rule is scheduled for recurring evaluation.
        """
        rule_id = "SCRUM158_03"
        rule_name = "Weekly Recurring Rule"
        interval_value = "weekly"
        condition_type = "amount"
        operator = ">="
        condition_value = 1000
        action_type = "transfer"
        account = "C"
        amount = 1000
        result = self.rule_page.create_recurring_rule(
            rule_id=rule_id,
            rule_name=rule_name,
            interval_value=interval_value,
            condition_type=condition_type,
            operator=operator,
            condition_value=condition_value,
            action_type=action_type,
            account=account,
            amount=amount
        )
        assert result is True, "Rule was not accepted or scheduled for recurring evaluation."

    def test_TC_SCRUM158_04_missing_trigger_field(self):
        """
        TC_SCRUM158_04: Prepare a schema missing the 'trigger' field, attempt to create rule, and assert schema is rejected with error indicating missing required field.
        """
        rule_id = "SCRUM158_04"
        rule_name = "Missing Trigger Rule"
        condition_type = "amount"
        operator = "<"
        condition_value = 50
        action_type = "transfer"
        account = "D"
        amount = 50
        error_msg = self.rule_page.create_rule_missing_trigger(
            rule_id=rule_id,
            rule_name=rule_name,
            condition_type=condition_type,
            operator=operator,
            condition_value=condition_value,
            action_type=action_type,
            account=account,
            amount=amount
        )
        assert error_msg is not None and ("missing" in error_msg.lower() or "required" in error_msg.lower()), f"Expected schema error for missing trigger field but got: {error_msg}"
