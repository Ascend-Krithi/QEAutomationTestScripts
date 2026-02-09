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

    def test_TC_SCRUM158_01_create_full_rule(self):
        """
        Test Case TC_SCRUM158_01: Prepare a JSON rule schema with all supported trigger, condition, and action types, submit, and validate.
        """
        rule_id = 'AUTO_TC158_01'
        rule_name = 'Full Rule - All Types'
        trigger_type = 'balance_above'
        date_value = '2026-02-10'
        interval = '7'
        after_deposit = True
        conditions = [{
            'type': 'balance',
            'threshold': '1000',
            'source': 'bank',
            'operator': 'greater_than'
        }]
        actions = [{
            'type': 'transfer',
            'amount': '500',
            'percentage': '50',
            'destination_account': 'ACC123456789'
        }]
        json_schema = '{"trigger": "balance_above", "conditions": [{"type": "balance", "threshold": 1000, "source": "bank", "operator": "greater_than"}], "actions": [{"type": "transfer", "amount": 500, "percentage": 50, "destination_account": "ACC123456789"}]}'
        success_message = self.page.create_rule(rule_id, rule_name, trigger_type, date_value, interval, after_deposit, conditions, actions, json_schema)
        assert 'success' in success_message.lower()

    def test_TC_SCRUM158_02_create_multi_condition_action_rule(self):
        """
        Test Case TC_SCRUM158_02: Prepare a rule schema with two conditions and two actions, submit, and validate logic.
        """
        rule_id = 'AUTO_TC158_02'
        rule_name = 'Multi Condition/Action Rule'
        trigger_type = 'balance_above'
        date_value = '2026-02-11'
        interval = '14'
        after_deposit = False
        conditions = [
            {
                'type': 'balance',
                'threshold': '2000',
                'source': 'bank',
                'operator': 'greater_than'
            },
            {
                'type': 'transaction',
                'threshold': '500',
                'source': 'atm',
                'operator': 'less_than'
            }
        ]
        actions = [
            {
                'type': 'transfer',
                'amount': '1000',
                'percentage': '',
                'destination_account': 'ACC987654321'
            },
            {
                'type': 'notify',
                'amount': '',
                'percentage': '',
                'destination_account': ''
            }
        ]
        json_schema = '{"trigger": "balance_above", "conditions": [{"type": "balance", "threshold": 2000, "source": "bank", "operator": "greater_than"}, {"type": "transaction", "threshold": 500, "source": "atm", "operator": "less_than"}], "actions": [{"type": "transfer", "amount": 1000, "destination_account": "ACC987654321"}, {"type": "notify"}]}'
        success_message = self.page.create_rule(rule_id, rule_name, trigger_type, date_value, interval, after_deposit, conditions, actions, json_schema)
        assert 'success' in success_message.lower()

    def test_TC_SCRUM158_03_create_rule_with_metadata(self):
        """
        Test Case TC_SCRUM158_03: Create a rule with metadata and validate metadata is stored.
        Steps:
        1. Prepare a rule schema with metadata fields (e.g., description, tags).
        2. Submit the schema.
        3. Retrieve the rule and check metadata.
        """
        rule_id = 'AUTO_TC158_03'
        rule_name = 'Rule With Metadata'
        trigger_type = 'balance_above'
        date_value = '2026-02-12'
        interval = '10'
        after_deposit = False
        conditions = [{
            'type': 'balance',
            'threshold': '1500',
            'source': 'bank',
            'operator': 'greater_than'
        }]
        actions = [{
            'type': 'transfer',
            'amount': '300',
            'percentage': '30',
            'destination_account': 'ACC111222333'
        }]
        metadata = {
            'description': 'Transfer rule',
            'tags': ['finance', 'auto']
        }
        schema_dict = {
            'trigger': trigger_type,
            'conditions': conditions,
            'actions': actions,
            'metadata': metadata
        }
        self.page.enter_rule_id(rule_id)
        self.page.enter_rule_name(rule_name)
        self.page.select_trigger_type(trigger_type)
        self.page.set_recurring_interval(interval)
        if after_deposit:
            self.page.toggle_after_deposit()
        self.page.set_json_schema(schema_dict)
        is_valid = self.page.validate_json_schema()
        assert is_valid, 'JSON schema with metadata should be valid.'
        # Simulate rule creation and retrieval
        # In a real test, you would submit and then retrieve via UI or API
        retrieved_metadata = self.page.get_metadata_from_rule(rule_id)
        assert retrieved_metadata is not None, 'Metadata should be present.'
        assert retrieved_metadata.get('description') == metadata['description']
        assert retrieved_metadata.get('tags') == metadata['tags']

    def test_TC_SCRUM158_04_schema_error_missing_trigger(self):
        """
        Test Case TC_SCRUM158_04: Submit a rule schema missing the 'trigger' field and validate error is returned.
        """
        rule_id = 'AUTO_TC158_04'
        rule_name = 'Schema Error Missing Trigger'
        # trigger_type is intentionally missing
        interval = '5'
        after_deposit = False
        conditions = [{
            'type': 'balance',
            'threshold': '900',
            'source': 'bank',
            'operator': 'greater_than'
        }]
        actions = [{
            'type': 'transfer',
            'amount': '100',
            'percentage': '10',
            'destination_account': 'ACC555666777'
        }]
        schema_dict = {
            # 'trigger' is omitted intentionally
            'conditions': conditions,
            'actions': actions
        }
        self.page.enter_rule_id(rule_id)
        self.page.enter_rule_name(rule_name)
        self.page.set_recurring_interval(interval)
        if after_deposit:
            self.page.toggle_after_deposit()
        self.page.set_json_schema(schema_dict)
        is_valid = self.page.validate_json_schema()
        assert not is_valid, 'JSON schema missing trigger should be invalid.'
        error_msg = self.page.get_schema_error()
        assert 'trigger' in error_msg.lower(), 'Error message should mention missing trigger field.'
