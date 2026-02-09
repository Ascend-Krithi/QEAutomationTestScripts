
{Import necessary modules}

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
        await self.login_page.fill_email('

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_TC_SCRUM158_01_create_rule_with_all_types(self):
        rule_schema = {
            "name": "AllTypesRule",
            "triggers": [
                {"type": "onCreate", "params": {}},
                {"type": "onUpdate", "params": {}},
                {"type": "onDelete", "params": {}}
            ],
            "conditions": [
                {"type": "fieldEquals", "field": "status", "value": "active"},
                {"type": "fieldContains", "field": "description", "value": "urgent"},
                {"type": "fieldGreaterThan", "field": "priority", "value": 5}
            ],
            "actions": [
                {"type": "sendEmail", "recipients": ["admin@example.com"], "subject": "Rule Triggered"},
                {"type": "createTask", "taskType": "followup", "assignee": "user1"},
                {"type": "logEvent", "message": "Rule executed successfully"}
            ]
        }
        response = await self.rule_page.submit_rule_schema_api(rule_schema)
        assert response.status_code == 201, f"Rule creation failed: {response.text}"
        rule_id = response.json().get("id")
        assert rule_id is not None, "Rule ID not returned after creation"
        created_rule = await self.rule_page.get_rule_from_db(rule_id)
        assert created_rule is not None, "Rule not found in database"
        assert created_rule["name"] == rule_schema["name"]
        assert len(created_rule["triggers"]) == len(rule_schema["triggers"])
        assert len(created_rule["conditions"]) == len(rule_schema["conditions"])
        assert len(created_rule["actions"]) == len(rule_schema["actions"])

    async def test_TC_SCRUM158_02_create_rule_with_two_conditions_and_actions(self):
        rule_schema = {
            "name": "TwoCondTwoActRule",
            "triggers": [
                {"type": "onUpdate", "params": {}}
            ],
            "conditions": [
                {"type": "fieldEquals", "field": "priority", "value": "high"},
                {"type": "fieldContains", "field": "description", "value": "escalate"}
            ],
            "actions": [
                {"type": "sendEmail", "recipients": ["support@example.com"], "subject": "Priority Escalated"},
                {"type": "createTask", "taskType": "escalation", "assignee": "team_lead"}
            ]
        }
        response = await self.rule_page.submit_rule_schema_api(rule_schema)
        assert response.status_code == 201, f"Rule creation failed: {response.text}"
        rule_id = response.json().get("id")
        assert rule_id is not None, "Rule ID not returned after creation"
        simulation_payload = {
            "rule_id": rule_id,
            "test_data": {
                "priority": "high",
                "description": "Please escalate this issue."
            }
        }
        simulation_result = await self.rule_page.simulate_rule_logic(simulation_payload)
        assert simulation_result["actions_executed"] == ["sendEmail", "createTask"], f"Unexpected actions executed: {simulation_result['actions_executed']}"
        assert simulation_result["conditions_met"] == True, "Conditions not met during simulation"

    async def test_TC_SCRUM158_03_create_rule_with_metadata(self):
        rule_id = "MetaRule01"
        rule_name = "MetaRule"
        metadata = {
            "description": "Transfer rule",
            "tags": ["finance", "auto"]
        }
        schema_text = '{"metadata": {"description": "Transfer rule", "tags": ["finance", "auto"]}, "triggers": [{"type": "onDeposit"}], "conditions": [{"type": "balanceThreshold", "value": 1000}], "actions": [{"type": "transfer", "amount": 500}]}'
        await self.rule_page.create_rule_with_metadata(rule_id, rule_name, metadata, schema_text)

    async def test_TC_SCRUM158_04_create_rule_missing_trigger(self):
        rule_id = "NoTriggerRule01"
        rule_name = "NoTriggerRule"
        schema_text = '{"conditions": [{"type": "balanceThreshold", "value": 1000}], "actions": [{"type": "transfer", "amount": 500}]}'
        await self.rule_page.create_rule_missing_trigger(rule_id, rule_name, schema_text)

    async def test_TC_SCRUM158_05_create_rule_with_invalid_trigger(self):
        rule_id = "InvalidTriggerRule01"
        rule_name = "InvalidTriggerRule"
        schema_text = '{"triggers": [{"type": "unknown_trigger"}], "conditions": [{"type": "balanceThreshold", "value": 1000}], "actions": [{"type": "transfer", "amount": 500}]}'
        await self.rule_page.create_rule_with_invalid_trigger(rule_id, rule_name, schema_text)

    async def test_TC_SCRUM158_06_create_rule_with_incomplete_condition(self):
        rule_id = "IncompleteConditionRule01"
        rule_name = "IncompleteConditionRule"
        schema_text = '{"triggers": [{"type": "onDeposit"}], "conditions": [{"type": "amount_above"}], "actions": [{"type": "transfer", "amount": 500}]}'
        await self.rule_page.create_rule_with_incomplete_condition(rule_id, rule_name, schema_text)
