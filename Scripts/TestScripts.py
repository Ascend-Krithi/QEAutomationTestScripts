import pytest

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
        await self.login_page.fill_email('

    # TC-FT-003: Rule with multiple conditions
    async def test_rule_with_multiple_conditions(self):
        # Step 1: Define a rule with multiple conditions
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 50},
            "conditions": [
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        }
        response = await self.page.submit_rule(rule_data)
        assert response["status"] == "accepted"

        # Step 2: Simulate a deposit from 'salary' when balance is 900
        deposit_data_low = {"balance": 900, "deposit": 100, "source": "salary"}
        result_low = await self.page.simulate_deposit(deposit_data_low)
        assert result_low["transfer_executed"] is False

        # Step 3: Simulate a deposit from 'salary' when balance is 1200
        deposit_data_high = {"balance": 1200, "deposit": 100, "source": "salary"}
        result_high = await self.page.simulate_deposit(deposit_data_high)
        assert result_high["transfer_executed"] is True

    # TC-FT-004: Validation error scenarios
    async def test_rule_missing_trigger_type(self):
        # Step 1: Submit a rule with missing trigger type
        rule_data_missing_trigger = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        response = await self.page.submit_rule(rule_data_missing_trigger)
        assert response["status"] == "error"
        assert "missing required field" in response["message"].lower()

    async def test_rule_unsupported_action_type(self):
        # Step 2: Submit a rule with unsupported action type
        rule_data_unsupported_action = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        response = await self.page.submit_rule(rule_data_unsupported_action)
        assert response["status"] == "error"
        assert "unsupported action type" in response["message"].lower()
