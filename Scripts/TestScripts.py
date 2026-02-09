import pytest
from Pages.LoginPage import LoginPage
from RuleEnginePage import RuleEnginePage

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

    async def test_specific_date_rule_trigger(self):
        # TC-FT-001: Define a JSON rule with trigger type 'specific_date' set to a future date
        rule = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()
        rule_engine.simulate_time_trigger("2024-07-01T10:00:00Z")
        assert rule_engine.verify_transfer_action(expected_count=1)

    async def test_recurring_weekly_rule_trigger(self):
        # TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly'
        rule = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()
        rule_engine.simulate_recurring_trigger(interval="weekly", times=3)
        assert rule_engine.verify_transfer_action_recurring(expected_intervals=3)
