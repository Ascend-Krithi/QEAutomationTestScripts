class TestLoginFunctionality:
    # ... existing methods ...

    def test_specific_date_trigger(self, selenium_driver):
        """Test Case 1: Define a JSON rule with trigger type 'specific_date' set to a future date, verify it is accepted, simulate system time to the trigger date, verify transfer action executes once."""
        from LoginPage import LoginPage
        import json
        import datetime
        import time

        login_page = LoginPage(selenium_driver)
        login_page.login_with_valid_credentials()

        # Define rule
        future_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        rule = {
            "trigger_type": "specific_date",
            "trigger_date": future_date,
            "action": "transfer"
        }
        rule_json = json.dumps(rule)

        # Submit rule and verify acceptance
        assert login_page.submit_rule(rule_json), "Rule submission failed"
        assert login_page.is_rule_accepted(rule_json), "Rule was not accepted"

        # Simulate system time to trigger date
        login_page.simulate_system_time(future_date)

        # Verify transfer action executes once
        assert login_page.is_transfer_executed_once(rule_json), "Transfer action did not execute once on specific date"

    def test_recurring_weekly_trigger(self, selenium_driver):
        """Test Case 2: Define a JSON rule with trigger type 'recurring' and interval 'weekly', verify it is accepted, simulate passing of weeks, verify transfer action executes at each interval."""
        from LoginPage import LoginPage
        import json
        import datetime

        login_page = LoginPage(selenium_driver)
        login_page.login_with_valid_credentials()

        # Define rule
        rule = {
            "trigger_type": "recurring",
            "interval": "weekly",
            "action": "transfer"
        }
        rule_json = json.dumps(rule)

        # Submit rule and verify acceptance
        assert login_page.submit_rule(rule_json), "Rule submission failed"
        assert login_page.is_rule_accepted(rule_json), "Rule was not accepted"

        # Simulate passing of weeks and verify transfer action executes at each interval
        start_date = datetime.datetime.now()
        for week in range(3):  # Simulate 3 weeks
            simulated_date = (start_date + datetime.timedelta(weeks=week)).strftime('%Y-%m-%d')
            login_page.simulate_system_time(simulated_date)
            assert login_page.is_transfer_executed_for_week(rule_json, week), f"Transfer action did not execute for week {week + 1}"
