
import unittest
from selenium import webdriver
from PageClasses.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.page = RuleConfigurationPage(self.driver)
        self.driver.get('https://your-app-url.com/rule-config')

    def tearDown(self):
        self.driver.quit()

    # Existing test methods...

    def test_TC_SCRUM158_03_recurring_interval_trigger_weekly(self):
        """TC_SCRUM158_03: Create schema with recurring interval trigger (weekly), amount >= 1000, transfer action to account C, submit, and verify scheduling logic."""
        schema_data = {
            "name": "Weekly Transfer Schema",
            "trigger": {
                "type": "recurring_interval",
                "interval": "weekly",
                "day_of_week": "Monday"
            },
            "amount": 1000,
            "action": {
                "type": "transfer",
                "to_account": "C"
            }
        }
        self.page.enter_schema_name(schema_data["name"])
        self.page.set_recurring_interval_trigger(
            interval=schema_data["trigger"]["interval"],
            day_of_week=schema_data["trigger"]["day_of_week"]
        )
        self.page.enter_amount(schema_data["amount"])
        self.page.select_transfer_action(schema_data["action"]["to_account"])
        self.page.submit_schema()
        success_msg = self.page.get_success_message()
        self.assertIn("scheduled weekly", success_msg.lower())
        self.assertTrue(self.page.verify_schedule_logic(interval="weekly", amount=1000, account="C"))

    def test_TC_SCRUM158_04_missing_trigger_schema_error(self):
        """TC_SCRUM158_04: Prepare schema missing the 'trigger' field, submit, and verify that the schema is rejected with an error indicating the missing required field."""
        schema_data = {
            "name": "Missing Trigger Schema",
            # 'trigger' intentionally omitted
            "amount": 500,
            "action": {
                "type": "transfer",
                "to_account": "C"
            }
        }
        self.page.enter_schema_name(schema_data["name"])
        self.page.enter_amount(schema_data["amount"])
        self.page.select_transfer_action(schema_data["action"]["to_account"])
        self.page.submit_schema()
        error_msg = self.page.get_error_message()
        self.assertIn("trigger", error_msg.lower())
        self.assertIn("required", error_msg.lower())

if __name__ == "__main__":
    unittest.main()