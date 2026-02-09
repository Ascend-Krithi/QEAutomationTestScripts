import pytest
from Pages.LoginPage import LoginPage

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
            "trigger_type": "specific_date",
            "trigger_date": "2099-12-31T00:00:00Z",
            "action": "transfer"
        }
        await self.login_page.navigate()
        await self.login_page.submit_rule(rule)
        # Simulate system time reaching that date
        await self.login_page.simulate_system_time("2099-12-31T00:00:00Z")
        assert await self.login_page.get_rule_status(rule) == "accepted"
        assert await self.login_page.get_action_status(rule) == "executed"

    async def test_recurring_weekly_rule_trigger(self):
        # TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly'
        rule = {
            "trigger_type": "recurring",
            "interval": "weekly",
            "action": "transfer"
        }
        await self.login_page.navigate()
        await self.login_page.submit_rule(rule)
        # Simulate passing of several weeks
        for week in range(1, 4):
            await self.login_page.simulate_system_time(f"2024-06-{7*week:02d}T00:00:00Z")
            assert await self.login_page.get_rule_status(rule) == "accepted"
            assert await self.login_page.get_action_status(rule) == "executed"
