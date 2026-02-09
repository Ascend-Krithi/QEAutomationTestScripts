
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

class TestRuleManagement:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleManagementPage(driver)

    async def test_create_rule_multiple_conditions_TC_FT_003(self):
        # Step 1: Define a rule with multiple conditions (balance >= 1000, source = 'salary')
        await self.rule_page.navigate_to_rule_management()
        rule_data = {
            'name': 'Salary Transfer Rule',
            'trigger_type': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000},
                {'field': 'source', 'operator': '=', 'value': 'salary'}
            ],
            'action_type': 'transfer',
            'action_params': {'amount': 500}
        }
        await self.rule_page.create_new_rule(rule_data)
        await self.rule_page.submit_rule()

        # Step 2: Simulate a deposit from 'salary' when balance is 900; expect transfer NOT executed
        await self.rule_page.simulate_deposit(source='salary', amount=900)
        transfer_executed = await self.rule_page.check_transfer_executed()
        assert not transfer_executed, 'Transfer should NOT be executed when balance < 1000'

        # Step 3: Simulate a deposit from 'salary' when balance is 1200; expect transfer executed
        await self.rule_page.simulate_deposit(source='salary', amount=1200)
        transfer_executed = await self.rule_page.check_transfer_executed()
        assert transfer_executed, 'Transfer should be executed when balance >= 1000 and source is salary'

    async def test_submit_rule_missing_invalid_fields_TC_FT_004(self):
        await self.rule_page.navigate_to_rule_management()
        # Step 1: Submit a rule with missing trigger type; expect error for missing required field
        rule_data_missing_trigger = {
            'name': 'Missing Trigger Rule',
            'trigger_type': '',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action_type': 'transfer',
            'action_params': {'amount': 100}
        }
        await self.rule_page.create_new_rule(rule_data_missing_trigger)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert 'trigger type is required' in error_msg.lower(), 'Expected error for missing trigger type'

        # Step 2: Submit a rule with unsupported action type; expect error for unsupported action type
        rule_data_invalid_action = {
            'name': 'Invalid Action Rule',
            'trigger_type': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action_type': 'unsupported_action',
            'action_params': {'amount': 100}
        }
        await self.rule_page.create_new_rule(rule_data_invalid_action)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert 'unsupported action type' in error_msg.lower(), 'Expected error for unsupported action type'

    # TC-FT-007: Batch rule upload and evaluation
    async def test_batch_rule_upload_and_evaluation_TC_FT_007(self):
        # Step 1: Upload batch of 10,000 valid rules
        batch_file_path = 'TestData/rules_batch_10000.json'  # Assume test data file exists
        self.rule_page.upload_rules_batch(batch_file_path)
        # Step 2: Validate batch upload count
        assert self.rule_page.validate_batch_upload(10000), 'Expected 10,000 rules uploaded.'
        # Step 3: Trigger evaluation for all rules
        self.rule_page.evaluate_all_rules()
        # Step 4: Check evaluation status
        status = self.rule_page.get_evaluation_status()
        assert status.get('passed', 0) >= 9990, 'Expected at least 9990 rules passed.'
        assert status.get('failed', 0) <= 10, 'Expected no more than 10 rules failed.'

    # TC-FT-008: SQL injection rejection
    async def test_sql_injection_rule_rejection_TC_FT_008(self):
        # Step 1: Submit rule with SQL injection in field value
        malicious_rule = '{"trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": [{"type": "balance_threshold", "value": "1000; DROP TABLE users;--"}]}'
        assert self.rule_page.check_sql_injection_rejection(malicious_rule), 'Expected SQL injection rule to be rejected.'
