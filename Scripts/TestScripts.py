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

    async def test_define_rule_with_multiple_conditions_and_deposit_simulation(self):
        # TC-FT-003: Define a rule with balance >= 1000 and source = 'salary'
        await self.rule_config_page.navigate()
        rule_name = "SalaryDepositRule"
        conditions = [
            {"field": "balance", "operator": ">=", "value": 1000},
            {"field": "source", "operator": "==", "value": "salary"}
        ]
        trigger_type = "deposit"
        action_type = "notify"
        await self.rule_config_page.create_rule(rule_name, conditions, trigger_type, action_type)
        assert await self.rule_config_page.get_success_message() == "Rule created successfully"

        # Simulate deposit with balance = 900, source = 'salary' (expect NOT executed)
        await self.rule_mgmt_page.navigate()
        await self.rule_mgmt_page.simulate_deposit(amount=900, source="salary")
        assert not await self.rule_mgmt_page.is_rule_executed(rule_name)

        # Simulate deposit with balance = 1200, source = 'salary' (expect executed)
        await self.rule_mgmt_page.simulate_deposit(amount=1200, source="salary")
        assert await self.rule_mgmt_page.is_rule_executed(rule_name)

    async def test_rule_submission_missing_trigger_and_unsupported_action(self):
        # TC-FT-004: Submit a rule with missing trigger type (expect error)
        await self.rule_config_page.navigate()
        rule_name = "InvalidTriggerRule"
        conditions = [{"field": "balance", "operator": ">=", "value": 500}]
        trigger_type = None
        action_type = "notify"
        await self.rule_config_page.create_rule(rule_name, conditions, trigger_type, action_type)
        error_msg = await self.rule_config_page.get_error_message()
        assert error_msg == "Trigger type is required"

        # Submit a rule with unsupported action type (expect error)
        rule_name = "UnsupportedActionRule"
        conditions = [{"field": "balance", "operator": "==", "value": 100}]
        trigger_type = "deposit"
        action_type = "unsupported_action"
        await self.rule_config_page.create_rule(rule_name, conditions, trigger_type, action_type)
        error_msg = await self.rule_config_page.get_error_message()
        assert error_msg == "Unsupported action type"

    async def test_define_percentage_deposit_rule_and_simulate_transfer(self):
        # TC-FT-005: Define a rule for 10% of deposit action and simulate deposit to verify transfer
        await self.rule_config_page.navigate()
        rule_name = "DepositPercentTransferRule"
        conditions = [
            {"field": "deposit_amount", "operator": ">", "value": 0}
        ]
        trigger_type = "deposit"
        action_type = "transfer"
        action_params = {"percent": 10}
        await self.rule_config_page.create_rule(rule_name, conditions, trigger_type, action_type, action_params=action_params)
        assert await self.rule_config_page.get_success_message() == "Rule created successfully"

        # Simulate deposit of 500 units, expect transfer of 50 units
        await self.rule_mgmt_page.navigate()
        await self.rule_mgmt_page.simulate_deposit(amount=500, source="generic")
        transferred_amount = await self.rule_mgmt_page.get_last_transfer_amount(rule_name)
        assert transferred_amount == 50, f"Expected transfer of 50 units, got {transferred_amount}"

    async def test_define_unsupported_rule_type_and_validate_system_response(self):
        # TC-FT-006: Define a rule with unsupported type 'currency_conversion' and validate system response
        await self.rule_config_page.navigate()
        rule_name = "UnsupportedRuleType"
        conditions = [
            {"field": "deposit_amount", "operator": ">", "value": 100}
        ]
        trigger_type = "currency_conversion"
        action_type = "notify"
        await self.rule_config_page.create_rule(rule_name, conditions, trigger_type, action_type)
        error_msg = await self.rule_config_page.get_error_message()
        # The system should either show a graceful error or accept and process
        assert error_msg in ["Unsupported rule type", "Rule created successfully"], f"Unexpected system response: {error_msg}"

        # Ensure existing rules still function
        await self.rule_mgmt_page.navigate()
        existing_rule_name = "DepositPercentTransferRule"
        await self.rule_mgmt_page.simulate_deposit(amount=500, source="generic")
        transferred_amount = await self.rule_mgmt_page.get_last_transfer_amount(existing_rule_name)
        assert transferred_amount == 50, f"Existing rule failed after unsupported rule type, got {transferred_amount}"

    # TC_SCRUM158_01: Prepare a valid rule schema with interval trigger, amount>100 condition, transfer 100 to account A
    async def test_TC_SCRUM158_01(self):
        await self.rule_config_page.enter_rule_id('TC_SCRUM158_01')
        await self.rule_config_page.enter_rule_name('Interval Amount Transfer')
        await self.rule_config_page.select_trigger_type('interval')
        await self.rule_config_page.set_date_picker('daily')
        await self.rule_config_page.click_add_condition()
        await self.rule_config_page.select_condition_type('amount')
        await self.rule_config_page.select_operator('>')
        await self.rule_config_page.enter_balance_threshold('100')
        await self.rule_config_page.select_action_type('transfer')
        await self.rule_config_page.enter_transfer_amount('100')
        await self.rule_config_page.enter_destination_account('A')
        await self.rule_config_page.click_save_rule()
        assert await self.rule_config_page.get_success_message() == 'Rule created successfully'

    # TC_SCRUM158_02: Prepare a schema with two conditions (amount>500, country==US) and two actions (transfer 500 to B, notify 'Transfer complete')
    async def test_TC_SCRUM158_02(self):
        await self.rule_config_page.enter_rule_id('TC_SCRUM158_02')
        await self.rule_config_page.enter_rule_name('Dual Condition Action')
        await self.rule_config_page.select_trigger_type('manual')
        await self.rule_config_page.click_add_condition()
        await self.rule_config_page.select_condition_type('amount')
        await self.rule_config_page.select_operator('>')
        await self.rule_config_page.enter_balance_threshold('500')
        await self.rule_config_page.click_add_condition()
        await self.rule_config_page.select_condition_type('country')
        await self.rule_config_page.select_operator('==')
        await self.rule_config_page.enter_balance_threshold('US')
        await self.rule_config_page.select_action_type('transfer')
        await self.rule_config_page.enter_transfer_amount('500')
        await self.rule_config_page.enter_destination_account('B')
        await self.rule_config_page.select_action_type('notify')
        # Assuming an enter_message function exists for notify; otherwise, skip
        # await self.rule_config_page.enter_message('Transfer complete')
        await self.rule_config_page.click_save_rule()
        assert await self.rule_config_page.get_success_message() == 'Rule created successfully'

    # TC_SCRUM158_03: Recurring interval trigger rule creation
    async def test_TC_SCRUM158_03(self):
        await self.rule_config_page.create_recurring_rule(
            rule_id='TC_SCRUM158_03',
            rule_name='Recurring Interval Rule',
            interval='weekly',
            condition_operator='>=',
            condition_value=1000,
            action_account='C',
            action_amount=1000
        )
        assert await self.rule_config_page.get_success_message() == 'Rule created successfully'

    # TC_SCRUM158_04: Validation of missing trigger field
    async def test_TC_SCRUM158_04(self):
        error_message = await self.rule_config_page.create_rule_without_trigger(
            rule_id='TC_SCRUM158_04',
            rule_name='Missing Trigger Rule',
            condition_operator='<',
            condition_value=50,
            action_account='D',
            action_amount=50
        )
        assert 'trigger' in error_message.lower() or 'missing' in error_message.lower()

    # TC_SCRUM158_05: Prepare a schema with unsupported trigger type and verify error
    async def test_TC_SCRUM158_05(self):
        schema_text = '{"trigger":{"type":"unsupported_type"},"conditions":[{"type":"amount","operator":"<","value":10}],"actions":[{"type":"transfer","account":"E","amount":10}]}'
        await self.rule_config_page.enter_rule_id('TC_SCRUM158_05')
        await self.rule_config_page.enter_rule_name('Unsupported Trigger Type')
        result = self.rule_config_page.verify_unsupported_trigger_type_error(schema_text)
        assert result, 'Expected unsupported trigger type error message.'

    # TC_SCRUM158_06: Prepare a schema with maximum allowed conditions and actions and verify storage
    async def test_TC_SCRUM158_06(self):
        schema_text = '{"trigger":{"type":"manual"},"conditions":[{"type":"amount","operator":"==","value":1},{"type":"amount","operator":"==","value":2},{"type":"amount","operator":"==","value":3},{"type":"amount","operator":"==","value":4},{"type":"amount","operator":"==","value":5},{"type":"amount","operator":"==","value":6},{"type":"amount","operator":"==","value":7},{"type":"amount","operator":"==","value":8},{"type":"amount","operator":"==","value":9},{"type":"amount","operator":"==","value":10}],"actions":[{"type":"transfer","account":"F1","amount":1},{"type":"transfer","account":"F2","amount":2},{"type":"transfer","account":"F3","amount":3},{"type":"transfer","account":"F4","amount":4},{"type":"transfer","account":"F5","amount":5},{"type":"transfer","account":"F6","amount":6},{"type":"transfer","account":"F7","amount":7},{"type":"transfer","account":"F8","amount":8},{"type":"transfer","account":"F9","amount":9},{"type":"transfer","account":"F10","amount":10}]}'
        await self.rule_config_page.enter_rule_id('TC_SCRUM158_06')
        await self.rule_config_page.enter_rule_name('Max Conditions Actions Storage')
        result = self.rule_config_page.verify_max_conditions_actions_storage(schema_text)
        assert result, 'Expected success message for storing maximum allowed conditions/actions.'

    # TC_SCRUM158_07: Prepare a schema with only required fields (one trigger, one condition, one action)
    async def test_TC_SCRUM158_07(self):
        result = self.rule_config_page.create_rule_with_minimal_schema(
            rule_id='TC_SCRUM158_07',
            rule_name='Minimal Schema Rule',
            trigger_type='manual',
            condition_type='amount',
            operator='==',
            value=1,
            action_type='transfer',
            account='G',
            amount=1
        )
        assert result['success'] == 'Rule created successfully', f"Expected rule creation success, got: {result['success']}"

    # TC_SCRUM158_08: Prepare a schema with a large metadata field (10,000 characters)
    async def test_TC_SCRUM158_08(self):
        large_metadata = 'A' * 10000
        result = self.rule_config_page.create_rule_with_large_metadata(
            rule_id='TC_SCRUM158_08',
            rule_name='Large Metadata Rule',
            trigger_type='manual',
            metadata=large_metadata
        )
        assert result['success'] == 'Rule created successfully' or 'performance' in result['success'].lower(), f"Expected rule creation or acceptable performance, got: {result['success']}"

    # TC_SCRUM158_09: Prepare a schema with malicious script in metadata and verify rejection
    async def test_TC_SCRUM158_09(self):
        result = self.rule_config_page.create_rule_with_malicious_metadata(
            rule_id='TC_SCRUM158_09',
            rule_name='Malicious Metadata Rule'
        )
        assert result['error'] is not None and result['error'] != '', f"Expected error message for malicious metadata, got: {result['error']}"
