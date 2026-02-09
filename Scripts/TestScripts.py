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
        await self.login_page.fill_email('')

class TestRuleConfiguration:
    def __init__(self, driver):
        self.page = RuleConfigurationPage(driver)

    def test_create_rule_schema_with_metadata(self):
        # Prepare metadata
        metadata = {'description': 'Transfer rule', 'tags': ['finance', 'auto']}
        # Create schema with metadata
        schema = self.page.create_rule_schema_with_metadata(metadata)
        # Submit schema
        success_msg = self.page.submit_schema()
        assert 'success' in success_msg.lower(), f"Submission failed: {success_msg}"
        # Retrieve rule and check metadata
        rule_id = schema['ruleId']
        assert self.page.retrieve_rule_and_check_metadata(rule_id, metadata)

    def test_create_invalid_schema_missing_trigger(self):
        # Create invalid schema missing 'trigger'
        schema = self.page.create_invalid_schema_missing_trigger()
        # Submit invalid schema and check error message
        error_msg = self.page.submit_invalid_schema()
        assert 'trigger' in error_msg.lower(), f"Expected error about missing trigger, got: {error_msg}"

    def test_TC_SCRUM158_05_invalid_trigger_schema(self):
        """
        TC_SCRUM158_05: Prepare a rule schema with invalid trigger value and submit. Expect error about invalid value.
        """
        # Prepare schema with invalid trigger
        schema = {
            'trigger': 'INVALID_TRIGGER',  # intentionally invalid
            'conditions': [{'type': 'amount', 'value': 100}],
            'actions': [{'type': 'notify'}]
        }
        error_msg = self.page.automate_invalid_trigger_schema(schema)
        assert 'invalid trigger' in error_msg.lower(), f"Expected error about invalid trigger, got: {error_msg}"

    def test_TC_SCRUM158_06_missing_condition_schema(self):
        """
        TC_SCRUM158_06: Prepare a rule schema with condition missing required parameters and submit. Expect error about incomplete condition.
        """
        # Prepare schema with missing condition parameters
        schema = {
            'trigger': 'transaction',
            'conditions': [{'type': 'amount'}],  # missing 'value' or other required fields
            'actions': [{'type': 'notify'}]
        }
        error_msg = self.page.automate_missing_condition_schema(schema)
        assert 'condition' in error_msg.lower() or 'parameter' in error_msg.lower(), f"Expected error about incomplete condition, got: {error_msg}"
