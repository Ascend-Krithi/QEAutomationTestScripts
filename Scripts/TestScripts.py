Import necessary modules

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
        await self.login_page.fill_email(''

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_config_page = RuleConfigurationPage(page)

    async def test_specific_date_trigger(self):
        # TC-FT-001: Define a JSON rule with trigger type 'specific_date' set to a future date. Simulate system time reaching the trigger date. Verify transfer action executed once.
        future_date = self.rule_config_page.get_future_date(days=7)
        rule_json = {
            "trigger": {
                "type": "specific_date",
                "date": future_date
            },
            "action": {
                "type": "transfer",
                "amount": 100,
                "destination": "AccountB"
            }
        }
        await self.rule_config_page.navigate()
        await self.rule_config_page.define_rule(rule_json)
        await self.rule_config_page.save_rule()
        await self.rule_config_page.simulate_system_time(future_date)
        executed_count = await self.rule_config_page.get_transfer_action_count(rule_json)
        assert executed_count == 1, f"Expected transfer action executed once, got {executed_count}"

    async def test_recurring_weekly_trigger(self):
        # TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly'. Simulate passing of several weeks. Verify transfer action executed at each interval.
        rule_json = {
            "trigger": {
                "type": "recurring",
                "interval": "weekly"
            },
            "action": {
                "type": "transfer",
                "amount": 50,
                "destination": "AccountC"
            }
        }
        await self.rule_config_page.navigate()
        await self.rule_config_page.define_rule(rule_json)
        await self.rule_config_page.save_rule()
        weeks_to_simulate = 4
        for i in range(weeks_to_simulate):
            await self.rule_config_page.simulate_system_time(self.rule_config_page.get_future_date(days=7*(i+1)))
        executed_count = await self.rule_config_page.get_transfer_action_count(rule_json)
        assert executed_count == weeks_to_simulate, f"Expected transfer action executed {weeks_to_simulate} times, got {executed_count}"
