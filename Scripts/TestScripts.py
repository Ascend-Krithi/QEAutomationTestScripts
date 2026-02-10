import asyncio
from RuleConfigurationPage import RuleConfigurationPage
from LoginPage import LoginPage
from datetime import datetime, timedelta

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
        await self.login_page.fill_email('')

# --- New Test Methods Appended Below ---

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_create_and_verify_rule_TC_SCRUM_158_001(self):
        pass

    async def test_rule_execution_and_log_TC_SCRUM_158_002(self):
        pass

    async def test_negative_rule_creation_TC_SCRUM_387_005(self):
        # Step 1: Missing required field 'rule_id'
        rule_data_missing_id = {
            "rule_name": "Incomplete Rule",
            "triggers": [],
            "conditions": [],
            "actions": []
        }
        self.rule_page.create_rule_with_invalid_data(rule_data_missing_id)
        self.rule_page.validate_error_response([
            {"message": "missing rule_id"}
        ])

        # Step 2: Empty triggers array
        rule_data_empty_triggers = {
            "rule_id": "R004",
            "triggers": [],
            "conditions": [{"field": "balance", "operator": ">", "value": 100}],
            "actions": [{"type": "transfer"}]
        }
        self.rule_page.create_rule_with_invalid_data(rule_data_empty_triggers)
        self.rule_page.validate_error_response([
            {"message": "at least one trigger is required"}
        ])

        # Step 3: Malformed condition (missing operator)
        rule_data_missing_operator = {
            "rule_id": "R005",
            "triggers": [{"type": "event"}],
            "conditions": [{"field": "balance", "value": 100}],
            "actions": [{"type": "transfer"}]
        }
        self.rule_page.create_rule_with_invalid_data(rule_data_missing_operator)
        self.rule_page.validate_error_response([
            {"message": "invalid condition structure"}
        ])

        # Step 4: Error response includes detailed validation messages
        error_response = {
            "errors": [
                {"field": "conditions[0].operator", "message": "operator is required"}
            ]
        }
        self.rule_page.validate_error_response(error_response["errors"])

    async def test_negative_rule_creation_TC_SCRUM_387_006(self):
        # Step 1: String value where number is expected in condition
        rule_data_invalid_amount_type = {
            "rule_id": "R006",
            "triggers": [{"type": "event"}],
            "conditions": [{"field": "amount", "operator": ">", "value": "invalid_number"}],
            "actions": [{"type": "transfer"}]
        }
        self.rule_page.create_rule_with_invalid_data(rule_data_invalid_amount_type)
        self.rule_page.verify_type_validation_error("amount", "number", "string")

        # Step 2: Number value where string is expected
        rule_data_id_type_mismatch = {
            "rule_id": 12345,
            "triggers": [{"type": "event"}],
            "conditions": [{"field": "status", "operator": "=", "value": "active"}],
            "actions": [{"type": "notify"}]
        }
        self.rule_page.create_rule_with_invalid_data(rule_data_id_type_mismatch)
        self.rule_page.verify_type_validation_error("rule_id", "string", "number")

        # Step 3: Array where object is expected for triggers
        rule_data_triggers_type_error = {
            "rule_id": "R007",
            "triggers": "invalid_array",
            "conditions": [{"field": "balance", "operator": ">", "value": 100}],
            "actions": [{"type": "transfer"}]
        }
        self.rule_page.create_rule_with_invalid_data(rule_data_triggers_type_error)
        self.rule_page.verify_type_validation_error("triggers", "array", "string")

        # Step 4: Error messages indicate expected vs actual types
        error_response_types = {
            "errors": [
                {"field": "triggers", "expected": "array", "received": "string"}
            ]
        }
        for err in error_response_types["errors"]:
            self.rule_page.verify_type_validation_error(err["field"], err["expected"], err["received"])
