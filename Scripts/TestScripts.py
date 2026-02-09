# Existing imports
from Pages.RuleConfigurationPage import RuleConfigurationPage
from selenium.webdriver.remote.webdriver import WebDriver

# Existing test class
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

# New tests for Rule Configuration Page
class TestRuleConfiguration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_define_specific_date_rule_and_execute(self):
        """
        TC-FT-001: Define JSON rule with 'specific_date' trigger, validate acceptance, simulate trigger, validate execution.
        """
        rule_data = {
            "trigger": {
                "type": "specific_date",
                "date": "2024-07-01T10:00:00Z"
            },
            "action": {
                "type": "fixed_amount",
                "amount": 100
            },
            "conditions": []
        }
        self.rule_page.define_json_rule(rule_data)
        self.rule_page.select_trigger_type("specific_date", date="2024-07-01T10:00:00Z")
        self.rule_page.save_rule()
        assert self.rule_page.validate_rule_acceptance(), "Rule was not accepted by the system."
        # Simulate system time reaching trigger date (UI validation)
        assert self.rule_page.simulate_trigger_action("SCENARIO-1"), "Transfer action was not executed at the specified date."
        assert self.rule_page.validate_rule_execution(), "Rule action was not executed."

    def test_define_recurring_rule_and_execute(self):
        """
        TC-FT-002: Define JSON rule with 'recurring' trigger, validate acceptance, simulate trigger, validate execution.
        """
        rule_data = {
            "trigger": {
                "type": "recurring",
                "interval": "weekly"
            },
            "action": {
                "type": "percentage_of_deposit",
                "percentage": 10
            },
            "conditions": []
        }
        self.rule_page.define_json_rule(rule_data)
        self.rule_page.select_trigger_type("recurring", interval="weekly")
        self.rule_page.save_rule()
        assert self.rule_page.validate_rule_acceptance(), "Rule was not accepted by the system."
        # Simulate passing of several weeks (UI validation)
        assert self.rule_page.simulate_trigger_action("SCENARIO-2"), "Transfer action was not executed at each interval."
        assert self.rule_page.validate_rule_execution(), "Rule action was not executed."
