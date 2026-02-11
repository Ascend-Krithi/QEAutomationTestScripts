# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

# --- Automated Transfers Rule Configuration Tests ---
class TestAutomatedTransfersRuleConfiguration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_TC_SCRUM_158_001(self):
        """
        Test Case TC-SCRUM-158-001: Create Automated Transfer Rule with specific date trigger, balance threshold condition, fixed transfer action, validate, save, and retrieve.
        """
        self.rule_page.open('https://app.example.com/rules/configuration')
        self.rule_page.set_rule_id('RULE-2505')
        self.rule_page.set_rule_name('Automated Transfer Dec31')
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_trigger_date('2024-12-31')
        self.rule_page.set_recurring_interval('')  # No interval for specific date
        self.rule_page.toggle_after_deposit()  # If needed
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold('500')
        self.rule_page.select_operator('greater_than')
        self.rule_page.select_transaction_source('Main Account')
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount('100')
        self.rule_page.set_destination_account('SAV-001')
        self.rule_page.edit_json_schema('{"trigger_type": "specific_date", "date": "2024-12-31T10:00:00Z", "condition_type": "balance_threshold", "operator": "greater_than", "amount": 500, "currency": "USD", "action_type": "fixed_transfer", "amount": 100, "currency": "USD", "destination_account": "SAV-001"}')
        self.rule_page.validate_schema()
        assert self.rule_page.is_schema_valid(), f"Schema validation failed: {self.rule_page.get_schema_error()}"
        self.rule_page.save_rule()
        success_msg = self.rule_page.get_success_message()
        assert 'saved successfully' in success_msg.lower(), f"Rule save failed: {success_msg}"
        # Retrieval/verification step would go here

    def test_TC_SCRUM_158_002(self):
        """
        Test Case TC-SCRUM-158-002: Create rule with specific date trigger (current date + 1 minute), balance > $300, transfer $50, execute and validate.
        """
        import datetime
        now = datetime.datetime.now()
        trigger_date = (now + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d')
        self.rule_page.open('https://app.example.com/rules/configuration')
        self.rule_page.set_rule_id('RULE-2506')
        self.rule_page.set_rule_name('AutoTransfer Soon')
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_trigger_date(trigger_date)
        self.rule_page.add_condition()
        self.rule_page.select_condition_type('balance_threshold')
        self.rule_page.set_balance_threshold('300')
        self.rule_page.select_operator('greater_than')
        self.rule_page.select_transaction_source('ACC-001')
        self.rule_page.select_action_type('fixed_transfer')
        self.rule_page.set_transfer_amount('50')
        self.rule_page.set_destination_account('SAV-001')
        self.rule_page.edit_json_schema('{"trigger_type": "specific_date", "date": "' + trigger_date + '", "condition_type": "balance_threshold", "operator": "greater_than", "amount": 300, "currency": "USD", "action_type": "fixed_transfer", "amount": 50, "currency": "USD", "destination_account": "SAV-001"}')
        self.rule_page.validate_schema()
        assert self.rule_page.is_schema_valid(), f"Schema validation failed: {self.rule_page.get_schema_error()}"
        self.rule_page.save_rule()
        success_msg = self.rule_page.get_success_message()
        assert 'saved successfully' in success_msg.lower(), f"Rule save failed: {success_msg}"
        # Retrieval/verification step would go here
