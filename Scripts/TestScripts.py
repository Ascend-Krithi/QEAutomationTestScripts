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

    # ... existing methods ...

    def test_bulk_load_and_evaluate_rules(self):
        """
        TC-FT-007: Load 10,000 valid rules and trigger evaluation for all rules.
        """
        # Generate 10,000 dummy valid rules
        rules = []
        for i in range(10000):
            rules.append({
                "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
                "action": {"type": "fixed_amount", "amount": 100},
                "conditions": [
                    {"type": "balance_threshold", "operator": ">=", "value": 1000}
                ]
            })
        loaded = self.rule_page.bulk_load_rules(rules)
        assert loaded, "Bulk load of 10,000 rules failed."
        evaluated = self.rule_page.trigger_evaluation_for_all_rules()
        assert evaluated, "Evaluation of all rules failed."

    def test_sql_injection_rule_rejection(self):
        """
        TC-FT-008: Submit a rule with SQL injection and validate rejection.
        """
        rule_with_sql_injection = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": [
                {"type": "balance_threshold", "value": "1000; DROP TABLE users;--"}
            ]
        }
        rejected = self.rule_page.submit_rule_with_sql_injection(rule_with_sql_injection)
        assert rejected, "SQL injection rule was not rejected as expected."
