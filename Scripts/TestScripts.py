# Existing Login Functionality Test Class

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

# Rule Configuration Test Cases
from Pages.RuleConfigurationPage import RuleConfigurationPage
import datetime

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_TC_SCRUM_158_001(self):
        # Step 1: Navigate to Automated Transfers rule creation interface
        # (Assume navigation done externally or add navigation code as needed)

        # Step 2: Define a specific date trigger for 2024-12-31 at 10:00 AM
        self.rule_page.enter_rule_id('RULE-2505')
        self.rule_page.enter_rule_name('Automated Transfer Rule - 2505')
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_specific_date_trigger('2024-12-31')
        self.rule_page.validate_json_schema()

        # Step 3: Add balance threshold condition: balance > $500
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold(500)
        self.rule_page.select_operator('greater_than')

        # Step 4: Add fixed amount transfer action: transfer $100 to savings account
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount(100)
        self.rule_page.set_destination_account('SAV-001')

        # Step 5: Save the complete rule
        self.rule_page.save_rule()
        assert self.rule_page.get_success_message() is not None

        # Step 6: Retrieve the saved rule and verify all components
        # (Assume retrieval method or add retrieval code as needed)
        # assert retrieved_rule matches expected

    def test_TC_SCRUM_158_002(self):
        # Step 1: Create a rule with specific date trigger (current date + 1 minute), balance > $300 condition, and transfer $50 action
        rule_id = 'RULE-2506'
        rule_name = 'Automated Transfer Rule - 2506'
        trigger_type = 'specific_date'
        trigger_date = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d')
        self.rule_page.enter_rule_id(rule_id)
        self.rule_page.enter_rule_name(rule_name)
        self.rule_page.select_trigger_type(trigger_type)
        self.rule_page.set_specific_date_trigger(trigger_date)
        self.rule_page.validate_json_schema()

        # Step 2: Add balance threshold condition: balance > $300
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold(300)
        self.rule_page.select_operator('greater_than')

        # Step 3: Add fixed amount transfer action: transfer $50 to savings account
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount(50)
        self.rule_page.set_destination_account('SAV-001')

        # Step 4: Save the complete rule
        self.rule_page.save_rule()
        assert self.rule_page.get_success_message() is not None

        # Step 5: Check rule execution log
        # (Assume log check method or add log check code as needed)

    def test_TC_SCRUM_387_005(self):
        """
        Test rule creation error scenarios:
        - missing rule_id
        - empty triggers
        - malformed condition
        - validation error details
        """
        # Step 1: Attempt to create rule without rule_id
        self.rule_page.enter_rule_id('')  # missing rule_id
        self.rule_page.enter_rule_name('Invalid Rule - Missing ID')
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_specific_date_trigger('2024-12-31')
        self.rule_page.validate_json_schema()
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold(500)
        self.rule_page.select_operator('greater_than')
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount(100)
        self.rule_page.set_destination_account('SAV-001')
        self.rule_page.save_rule()
        error_msg = self.rule_page.get_error_message()
        assert error_msg is not None
        assert 'rule_id' in error_msg or 'Mandatory' in error_msg

        # Step 2: Attempt to create rule with empty triggers
        self.rule_page.enter_rule_id('RULE-387-005-2')
        self.rule_page.enter_rule_name('Invalid Rule - Empty Trigger')
        self.rule_page.select_trigger_type('')  # empty trigger
        self.rule_page.set_specific_date_trigger('')
        self.rule_page.validate_json_schema()
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold(500)
        self.rule_page.select_operator('greater_than')
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount(100)
        self.rule_page.set_destination_account('SAV-001')
        self.rule_page.save_rule()
        error_msg = self.rule_page.get_error_message()
        assert error_msg is not None
        assert 'trigger' in error_msg or 'Mandatory' in error_msg

        # Step 3: Attempt to create rule with malformed condition
        self.rule_page.enter_rule_id('RULE-387-005-3')
        self.rule_page.enter_rule_name('Invalid Rule - Malformed Condition')
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_specific_date_trigger('2024-12-31')
        self.rule_page.validate_json_schema()
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold('not_a_number')  # malformed
        self.rule_page.select_operator('greater_than')
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount(100)
        self.rule_page.set_destination_account('SAV-001')
        self.rule_page.save_rule()
        error_msg = self.rule_page.get_error_message()
        assert error_msg is not None
        assert 'condition' in error_msg or 'invalid' in error_msg or 'number' in error_msg

        # Step 4: Validate error details returned by API/UI
        # (Assume get_error_details returns structured error info)
        error_details = self.rule_page.get_error_details()
        assert error_details is not None
        assert 'validation' in error_details or 'details' in error_details

    def test_TC_SCRUM_387_006(self):
        """
        Test rule creation error scenarios:
        - type mismatch
        - invalid array
        - validation error details
        """
        # Step 1: Attempt to create rule with type mismatch (e.g., string instead of integer for balance)
        self.rule_page.enter_rule_id('RULE-387-006-1')
        self.rule_page.enter_rule_name('Invalid Rule - Type Mismatch')
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_specific_date_trigger('2024-12-31')
        self.rule_page.validate_json_schema()
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold('five_hundred')  # type mismatch
        self.rule_page.select_operator('greater_than')
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount(100)
        self.rule_page.set_destination_account('SAV-001')
        self.rule_page.save_rule()
        error_msg = self.rule_page.get_error_message()
        assert error_msg is not None
        assert 'type' in error_msg or 'invalid' in error_msg or 'number' in error_msg

        # Step 2: Attempt to create rule with invalid array (e.g., empty conditions array)
        self.rule_page.enter_rule_id('RULE-387-006-2')
        self.rule_page.enter_rule_name('Invalid Rule - Empty Conditions Array')
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_specific_date_trigger('2024-12-31')
        self.rule_page.validate_json_schema()
        # Do not add any condition
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount(100)
        self.rule_page.set_destination_account('SAV-001')
        self.rule_page.save_rule()
        error_msg = self.rule_page.get_error_message()
        assert error_msg is not None
        assert 'conditions' in error_msg or 'array' in error_msg or 'empty' in error_msg

        # Step 3: Validate error details returned by API/UI
        error_details = self.rule_page.get_error_details()
        assert error_details is not None
        assert 'validation' in error_details or 'details' in error_details
