import asyncio
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.RuleManagementPage import RuleManagementPage

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
    def __init__(self, page):
        self.page = page
        self.rule_config_page = RuleConfigurationPage(page)
        self.rule_mgmt_page = RuleManagementPage(page)

    # ...[existing async test methods]...

    async def test_TC_SCRUM158_09(self):
        '''
        TC_SCRUM158_09: Prepare a schema with malicious metadata and verify error response.
        '''
        malicious_schema = '{"trigger":{"type":"manual"},"conditions":[{"type":"amount","operator":"==","value":1}],"actions":[{"type":"transfer","account":"I","amount":1}],"metadata":"<script>alert(\'hack\')</script>"}'
        self.rule_config_page.prepare_schema_with_malicious_metadata(malicious_schema)
        self.rule_config_page.submit_schema()
        error_msg = self.rule_config_page.get_error_message()
        assert any(keyword in error_msg.lower() for keyword in ['invalid', 'error', 'malicious']), f"Expected error indication for malicious metadata, got: {error_msg}"

    async def test_TC_FT_003_rule_with_multiple_conditions(self):
        '''
        TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary'), simulate deposits, and verify transfer execution.
        '''
        rule_data = {
            'ruleId': 'TCFT003',
            'ruleName': 'Multiple Conditions Rule',
            'trigger': {'type': 'after_deposit'},
            'action': {'type': 'fixed_amount', 'amount': 50},
            'conditions': [
                {'type': 'balance_threshold', 'operator': '>=', 'value': 1000},
                {'type': 'transaction_source', 'value': 'salary'}
            ]
        }
        # Define rule
        self.rule_config_page.define_rule_with_multiple_conditions(rule_data)
        assert self.rule_config_page.verify_rule_accepted()
        # Simulate deposit with balance 900 (should NOT execute transfer)
        self.rule_config_page.simulate_deposit(balance=900, deposit=100, source='salary')
        assert self.rule_config_page.verify_transfer_not_executed()
        # Simulate deposit with balance 1200 (should execute transfer)
        self.rule_config_page.simulate_deposit(balance=1200, deposit=100, source='salary')
        assert self.rule_config_page.verify_transfer_executed()

    async def test_TC_FT_004_rule_validation(self):
        '''
        TC-FT-004: Submit rules with missing trigger and unsupported action, verify errors.
        '''
        # Missing trigger
        rule_data_missing_trigger = {
            'ruleName': 'Missing Trigger Rule',
            'action': {'type': 'fixed_amount', 'amount': 100},
            'conditions': []
        }
        self.rule_config_page.submit_rule_with_missing_trigger(rule_data_missing_trigger)
        assert self.rule_config_page.verify_missing_trigger_error()
        # Unsupported action
        rule_data_unsupported_action = {
            'ruleName': 'Unsupported Action Rule',
            'trigger': {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'},
            'action': {'type': 'unknown_action'},
            'conditions': []
        }
        self.rule_config_page.submit_rule_with_unsupported_action(rule_data_unsupported_action)
        assert self.rule_config_page.verify_unsupported_action_error()
