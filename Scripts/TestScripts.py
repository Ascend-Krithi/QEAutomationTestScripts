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

    def test_TC_SCRUM158_05_invalid_trigger_rule(self):
        """
        Test Case TC_SCRUM158_05: Prepare a rule schema with an invalid trigger value and submit. Expect error about invalid value.
        """
        error_message = self.page.create_rule_with_invalid_trigger()
        assert 'invalid' in error_message.lower() or 'unknown' in error_message.lower()

    def test_TC_SCRUM158_06_missing_condition_param_rule(self):
        """
        Test Case TC_SCRUM158_06: Prepare a rule schema with a condition missing required parameters and submit. Expect error about incomplete condition.
        """
        error_message = self.page.create_rule_with_missing_condition_param()
        assert 'missing' in error_message.lower() or 'required' in error_message.lower()
