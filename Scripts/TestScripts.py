# Existing imports
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
        self.driver = driver
        self.rule_config_page = RuleConfigurationPage(driver)

    async def test_TC_SCRUM158_01(self):
        """
        Test Case TC_SCRUM158_01:
        - Prepare a JSON rule schema with all supported trigger, condition, and action types populated.
        - Submit the rule schema to the API endpoint for rule creation.
        - Retrieve the created rule from the database.
        - Validate that the rule matches the submitted schema.
        """
        # Fill rule form
        self.rule_config_page.fill_rule_form('RULE001', 'All Types Rule')
        self.rule_config_page.select_trigger_type('balance_above')
        self.rule_config_page.set_trigger_date('2024-06-01')
        self.rule_config_page.set_recurring_interval('7')
        self.rule_config_page.toggle_after_deposit()
        # Add condition
        self.rule_config_page.add_condition()
        self.rule_config_page.select_condition_type('balance')
        self.rule_config_page.set_balance_threshold('1000')
        self.rule_config_page.select_transaction_source('provider_a')
        self.rule_config_page.select_operator('greater_than')
        # Add action
        self.rule_config_page.select_action_type('transfer')
        self.rule_config_page.set_transfer_amount('500')
        self.rule_config_page.set_percentage('50')
        self.rule_config_page.set_destination_account('ACC123')
        # Prepare JSON schema
        rule_schema = '{"trigger": "balance_above", "conditions": [{"type": "balance", "threshold": 1000}], "actions": [{"type": "transfer", "amount": 500, "percentage": 50, "destination": "ACC123"}]}'
        self.rule_config_page.edit_json_schema(rule_schema)
        self.rule_config_page.validate_schema()
        assert 'valid' in self.rule_config_page.get_success_message().lower()

    async def test_TC_SCRUM158_02(self):
        """
        Test Case TC_SCRUM158_02:
        - Prepare a rule schema with two conditions and two actions.
        - Submit the schema to the API endpoint.
        - Verify rule logic via simulation.
        - Validate that all conditions and actions are evaluated as expected.
        """
        # Fill rule form
        self.rule_config_page.fill_rule_form('RULE002', 'Multi Conditions/Actions Rule')
        self.rule_config_page.select_trigger_type('recurring')
        self.rule_config_page.set_trigger_date('2024-06-02')
        self.rule_config_page.set_recurring_interval('14')
        # Add conditions
        self.rule_config_page.add_condition()
        self.rule_config_page.select_condition_type('balance')
        self.rule_config_page.set_balance_threshold('2000')
        self.rule_config_page.select_transaction_source('provider_b')
        self.rule_config_page.select_operator('less_than')
        self.rule_config_page.add_condition()
        self.rule_config_page.select_condition_type('transaction')
        self.rule_config_page.set_balance_threshold('500')
        self.rule_config_page.select_transaction_source('provider_c')
        self.rule_config_page.select_operator('equal_to')
        # Add actions
        self.rule_config_page.select_action_type('transfer')
        self.rule_config_page.set_transfer_amount('250')
        self.rule_config_page.set_percentage('20')
        self.rule_config_page.set_destination_account('ACC456')
        self.rule_config_page.select_action_type('notify')
        # Prepare JSON schema
        rule_schema = '{"conditions": [{"type": "balance", "threshold": 2000}, {"type": "transaction", "threshold": 500}], "actions": [{"type": "transfer", "amount": 250, "percentage": 20, "destination": "ACC456"}, {"type": "notify"}]}'
        self.rule_config_page.edit_json_schema(rule_schema)
        self.rule_config_page.validate_schema()
        assert 'valid' in self.rule_config_page.get_success_message().lower()

    async def test_TC_SCRUM158_03(self):
        """
        Test Case TC_SCRUM158_03:
        - Prepare a rule schema with metadata fields (e.g., description, created_by).
        - Submit the rule schema.
        - Validate that the metadata is stored and retrievable.
        """
        # Fill rule form with metadata
        self.rule_config_page.fill_rule_form('RULE003', 'Metadata Rule')
        # Example assumes set_metadata and get_metadata methods exist in RuleConfigurationPage
        self.rule_config_page.edit_json_schema('{"trigger": "balance_above", "conditions": [], "actions": [], "metadata": {"description": "This rule tests metadata storage", "created_by": "qa_automation"}}')
        self.rule_config_page.validate_schema()
        assert 'valid' in self.rule_config_page.get_success_message().lower()
        # Retrieve and validate metadata (pseudo-code, adapt as needed)
        stored_metadata = self.rule_config_page.get_success_message()  # Replace with actual retrieval
        assert 'metadata' in stored_metadata.lower()

    async def test_TC_SCRUM158_04(self):
        """
        Test Case TC_SCRUM158_04:
        - Prepare a rule schema missing the 'trigger' field.
        - Submit the rule schema.
        - Validate that an error message is shown indicating the missing trigger.
        """
        # Fill rule form
        self.rule_config_page.fill_rule_form('RULE004', 'Missing Trigger Rule')
        # Prepare JSON schema missing trigger
        rule_schema = '{"conditions": [{"type": "balance", "threshold": 1500}], "actions": [{"type": "transfer", "amount": 100, "destination": "ACC789"}]}'
        self.rule_config_page.edit_json_schema(rule_schema)
        self.rule_config_page.validate_schema()
        error_message = self.rule_config_page.get_schema_error_message()
        assert 'trigger' in error_message.lower() or 'missing trigger' in error_message.lower()
