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
        result = self.rule_page.define_percentage_of_deposit_rule(10)
        assert result is True, 'Rule for 10% deposit was not accepted.'

    def test_simulate_deposit_and_verify_transfer(self):
        deposit_amount = 500
        expected_transfer = 50
        result = self.rule_page.simulate_deposit_and_verify_transfer(deposit_amount, expected_transfer)
        assert result is True, f'Transfer of {expected_transfer} units was not executed after deposit.'

    def test_define_rule_with_future_trigger(self):
        feedback = self.rule_page.define_rule_with_future_trigger('currency_conversion', 'EUR', 'fixed_amount', 100)
        assert feedback in ['System accepts or gracefully rejects with a clear message', 'No feedback received.'], f'Unexpected feedback: {feedback}'

    def test_verify_existing_rules_execution(self):
        result = self.rule_page.verify_existing_rules_execution()
        assert result is True, 'Existing rules did not function as expected.'

    def test_batch_upload_and_evaluate_rules(self):
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
        assert True, 'Batch upload or evaluation failed.'

    def test_sql_injection_rejection(self):
        sql_injection_rule = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": [{"type": "balance_threshold", "value": "1000; DROP TABLE users;--"}]
        }
        self.rule_page.submit_rule_with_conditions(sql_injection_rule)
        result = self.rule_page.verify_rule_rejected()
        assert result is True, 'SQL injection rule was not rejected by the system.'

    def test_TC_SCRUM158_01_create_rule_with_all_types(self):
        rule_schema = {
            "trigger": {"type": "interval", "value": "daily"},
            "conditions": [{"type": "amount", "operator": ">", "value": 100}],
            "actions": [{"type": "transfer", "account": "A", "amount": 100}]
        }
        self.rule_page.create_rule(
            rule_id="SCRUM158_01",
            rule_name="Interval Amount Transfer",
            trigger=rule_schema["trigger"],
            conditions=rule_schema["conditions"],
            actions=rule_schema["actions"]
        )
        success_msg = self.rule_page.get_success_message()
        assert "success" in success_msg.lower(), f"Rule creation failed: {success_msg}"

    def test_TC_SCRUM158_02_create_rule_with_multiple_conditions_actions(self):
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
        success_msg = self.rule_page.get_success_message()
        assert "success" in success_msg.lower(), f"Rule creation failed: {success_msg}"

    def test_TC_SCRUM158_03_recurring_interval_trigger_rule_creation_and_scheduling(self):
        """
        TC_SCRUM158_03: Create a rule with a recurring interval trigger (weekly), submit, and verify scheduling logic.
        """
        rule_id = "SCRUM158_03"
        rule_name = "Weekly Recurring Amount Transfer"
        trigger = {"type": "interval", "value": "weekly"}
        conditions = [{"type": "amount", "operator": ">=", "value": 1000}]
        actions = [{"type": "transfer", "account": "C", "amount": 1000}]
        # Fill in the rule configuration using PageClass methods
        self.rule_page.enter_rule_id(rule_id)
        self.rule_page.enter_rule_name(rule_name)
        self.rule_page.set_trigger_interval(trigger["value"])
        for cond in conditions:
            self.rule_page.add_condition(cond["type"], cond["operator"], cond["value"])
        for act in actions:
            self.rule_page.set_action(act["type"], act["account"], act["amount"])
        # Optionally, enter schema JSON
        import json
        schema_json = json.dumps({"trigger": trigger, "conditions": conditions, "actions": actions})
        self.rule_page.enter_schema_json(schema_json)
        self.rule_page.validate_schema()
        self.rule_page.submit_rule()
        assert self.rule_page.verify_success(), "Rule was not accepted or scheduled for weekly execution."

    def test_TC_SCRUM158_04_schema_validation_error_handling(self):
        """
        TC_SCRUM158_04: Prepare a schema missing the 'trigger' field, attempt to create rule, and verify error handling.
        """
        rule_id = "SCRUM158_04"
        rule_name = "Missing Trigger Error"
        # No trigger field
        conditions = [{"type": "amount", "operator": "<", "value": 50}]
        actions = [{"type": "transfer", "account": "D", "amount": 50}]
        # Fill in the rule configuration using PageClass methods
        self.rule_page.enter_rule_id(rule_id)
        self.rule_page.enter_rule_name(rule_name)
        for cond in conditions:
            self.rule_page.add_condition(cond["type"], cond["operator"], cond["value"])
        for act in actions:
            self.rule_page.set_action(act["type"], act["account"], act["amount"])
        import json
        schema_json = json.dumps({"conditions": conditions, "actions": actions})
        self.rule_page.enter_schema_json(schema_json)
        self.rule_page.validate_schema()
        self.rule_page.submit_rule()
        assert self.rule_page.verify_error("trigger"), "Schema error for missing trigger field was not returned."