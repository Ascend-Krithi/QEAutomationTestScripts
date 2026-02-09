# Import necessary modules
from Pages.RuleEnginePage import RuleEnginePage

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
        # ... (rest of original logic)

class TestRuleEngine:
    def __init__(self, driver):
        self.driver = driver
        self.rule_engine = RuleEnginePage(driver)

    def test_specific_date_rule(self):
        rule_json = '{"trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": []}'
        self.rule_engine.enter_rule(rule_json)
        self.rule_engine.submit_rule()
        acceptance = self.rule_engine.wait_for_rule_acceptance()
        assert 'accepted' in acceptance.lower()
        self.rule_engine.simulate_time('2024-07-01T10:00:00Z')
        assert self.rule_engine.verify_transfer_executed(expected_count=1)

    def test_recurring_weekly_rule(self):
        rule_json = '{"trigger": {"type": "recurring", "interval": "weekly"}, "action": {"type": "percentage_of_deposit", "percentage": 10}, "conditions": []}'
        self.rule_engine.enter_rule(rule_json)
        self.rule_engine.submit_rule()
        acceptance = self.rule_engine.wait_for_rule_acceptance()
        assert 'accepted' in acceptance.lower()
        # Simulate several weeks (stub, depends on backend/test hooks)
        for _ in range(4):
            self.rule_engine.simulate_time('weekly')
        assert self.rule_engine.verify_recurring_transfer(interval='weekly', occurrences=4)
