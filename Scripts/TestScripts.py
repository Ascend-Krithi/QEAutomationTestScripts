import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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
        self.rule_page = RuleConfigurationPage(driver)

    def test_create_rule_with_specific_date_trigger(self):
        rule_id = "TC-FT-001"
        rule_name = "Specific Date Trigger Rule"
        date_str = "2024-07-01"
        amount = 100
        destination_account = "ACC-12345"
        rule_json = '{"trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": []}'
        self.rule_page.create_rule_with_specific_date_trigger(rule_id, rule_name, date_str, amount, destination_account, rule_json)
        self.rule_page.validate_rule_schema()
        assert self.rule_page.is_success_message_displayed(), "Rule should be accepted by the system."
        time.sleep(2)

    def test_create_rule_with_recurring_trigger(self):
        rule_id = "TC-FT-002"
        rule_name = "Recurring Weekly Trigger Rule"
        interval = "weekly"
        percentage = 10
        destination_account = "ACC-67890"
        rule_json = '{"trigger": {"type": "recurring", "interval": "weekly"}, "action": {"type": "percentage_of_deposit", "percentage": 10}, "conditions": []}'
        self.rule_page.create_rule_with_recurring_trigger(rule_id, rule_name, interval, percentage, destination_account, rule_json)
        self.rule_page.validate_rule_schema()
        assert self.rule_page.is_success_message_displayed(), "Rule should be accepted by the system."
        for _ in range(3):
            time.sleep(2)

    def test_TC_SCRUM158_01(self):
        rule_id = "TC_SCRUM158_01"
        rule_name = "Interval Daily Rule"
        trigger_types = ["interval"]
        trigger_date = None
        interval = "daily"
        after_deposit = False
        conditions = [{"type": "amount", "operator": ">", "balance_threshold": 100}]
        actions = [{"type": "transfer", "transfer_amount": 100, "destination_account": "A"}]
        self.rule_page.prepare_and_submit_full_rule_schema_and_verify(rule_id, rule_name, trigger_types, trigger_date, interval, after_deposit, conditions, actions)
        success_msg = self.rule_page.get_success_message()
        assert "success" in success_msg.lower(), f"Rule creation failed: {success_msg}"

    def test_TC_SCRUM158_02(self):
        rule_id = "TC_SCRUM158_02"
        rule_name = "Manual Multi-Condition Multi-Action Rule"
        conditions = [
            {"type": "amount", "operator": ">", "balance_threshold": 500},
            {"type": "country", "operator": "==", "transaction_source": "US"}
        ]
        actions = [
            {"type": "transfer", "transfer_amount": 500, "destination_account": "B"},
            {"type": "notify", "message": "Transfer complete"}
        ]
        self.rule_page.prepare_and_submit_multi_condition_action_rule_and_verify(rule_id, rule_name, conditions, actions)
        success_msg = self.rule_page.get_success_message()
        assert "success" in success_msg.lower(), f"Rule creation failed: {success_msg}"

    def test_TC_SCRUM158_03(self):
        rule_id = "TC_SCRUM158_03"
        rule_name = "Recurring Weekly Amount Rule"
        interval = "weekly"
        condition_operator = ">="
        condition_value = 1000
        action_account = "C"
        action_amount = 1000
        self.rule_page.create_recurring_rule(rule_id, rule_name, interval, condition_operator, condition_value, action_account, action_amount)
        self.rule_page.validate_json_schema()
        success_msg = self.rule_page.get_success_message()
        assert "accepted" in success_msg.lower() or "scheduled" in success_msg.lower(), f"Rule not scheduled: {success_msg}"
        time.sleep(2)

    def test_TC_SCRUM158_04(self):
        rule_id = "TC_SCRUM158_04"
        rule_name = "Missing Trigger Rule"
        condition_operator = "<"
        condition_value = 50
        action_account = "D"
        action_amount = 50
        self.rule_page.create_rule_missing_trigger(rule_id, rule_name, condition_operator, condition_value, action_account, action_amount)
        self.rule_page.validate_json_schema()
        error_msg = self.rule_page.get_schema_error_message()
        assert "missing" in error_msg.lower() or "required" in error_msg.lower(), f"Schema error not detected: {error_msg}"
        time.sleep(2)
