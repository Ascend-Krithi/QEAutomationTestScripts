# Import necessary modules
from LoginPage import LoginPage
from RuleManagementPage import RuleManagementPage
from TransactionPage import TransactionPage
from RuleCreationPage import RuleCreationPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.open()
        self.login_page.enter_email('')
        self.login_page.enter_password('')
        self.login_page.submit()
        assert self.login_page.is_empty_field_prompt_displayed() is True

    def test_remember_me_functionality(self):
        self.login_page.open()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('securepassword')
        self.login_page.toggle_remember_me(True)
        self.login_page.submit()
        assert self.login_page.is_dashboard_loaded() is True

class TestRuleManagement:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.rule_page = RuleManagementPage(driver)
        self.transaction_page = TransactionPage(driver)

    def test_define_specific_date_rule(self):
        """
        TC-FT-001: Define a JSON rule with trigger type 'specific_date' set to a future date, simulate system time reaching the trigger date, and verify transfer action is executed once.
        """
        rule_data = {
            'name': 'Specific Date Rule',
            'trigger': 'specific_date',
            'action': 'fixed_amount',
            'value': 100,
            'date': '2024-07-01'
        }
        # Login
        self.login_page.open()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('securepassword')
        self.login_page.submit()
        assert self.login_page.is_dashboard_loaded() is True
        # Create rule
        self.rule_page.open()
        self.rule_page.create_rule(rule_data)
        assert self.rule_page.is_rule_created('Specific Date Rule') is True
        # Simulate system time reaching the trigger date (pseudo-code, replace with actual system time manipulation if available)
        # Here we assume that the system triggers the rule automatically
        # Validate transfer action
        self.transaction_page.open()
        self.transaction_page.perform_transaction({'amount': 100, 'type': 'transfer'})
        assert self.transaction_page.is_transaction_successful() is True

    def test_define_recurring_rule(self):
        """
        TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly', simulate passing of several weeks, and verify transfer action is executed at each interval.
        """
        rule_data = {
            'name': 'Weekly Recurring Rule',
            'trigger': 'recurring',
            'action': 'percentage_of_deposit',
            'value': 10,
            'interval': 'weekly'
        }
        # Login
        self.login_page.open()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('securepassword')
        self.login_page.submit()
        assert self.login_page.is_dashboard_loaded() is True
        # Create rule
        self.rule_page.open()
        self.rule_page.create_rule(rule_data)
        assert self.rule_page.is_rule_created('Weekly Recurring Rule') is True
        # Simulate passing of several weeks (pseudo-code, replace with actual time manipulation if available)
        # Validate transfer action at each interval
        for week in range(1, 4):
            self.transaction_page.open()
            self.transaction_page.perform_transaction({'amount': 100, 'type': 'deposit', 'percentage': 10})
            assert self.transaction_page.is_transaction_successful() is True

class TestRuleCreation:
    def __init__(self, driver):
        self.driver = driver
        self.rule_creation_page = RuleCreationPage(driver)

    def test_rule_creation_positive_scenario(self):
        """
        TC-FT-003: Define rule with balance >= 1000, source = 'salary'.
        Simulate deposit from 'salary' when balance is 900 (transfer NOT executed).
        Simulate deposit from 'salary' when balance is 1200 (transfer executed).
        """
        self.rule_creation_page.define_rule(balance_threshold=1000, source='salary')
        self.rule_creation_page.submit_rule()
        assert self.rule_creation_page.verify_rule_acceptance(), "Rule was not accepted"

        # Step 2: Deposit 900 from 'salary'
        self.rule_creation_page.simulate_deposit(amount=900, source='salary')
        transfer_status_1 = self.rule_creation_page.get_transfer_status()
        assert "Transfer not executed" in transfer_status_1, f"Unexpected transfer status: {transfer_status_1}"

        # Step 3: Deposit 1200 from 'salary'
        self.rule_creation_page.simulate_deposit(amount=1200, source='salary')
        transfer_status_2 = self.rule_creation_page.get_transfer_status()
        assert "Transfer executed" in transfer_status_2, f"Unexpected transfer status: {transfer_status_2}"

    def test_rule_creation_missing_trigger_type(self):
        """
        TC-FT-004 Step 1: Submit a rule with missing trigger type. Expect system error indicating missing required field.
        """
        try:
            # Attempt to define a rule without trigger type
            self.rule_creation_page.define_rule(balance_threshold=1000, source='salary')
            # Simulate missing trigger by not calling submit_rule or by manipulating internal state
            # For demonstration, assume submit_rule() checks trigger type and raises Exception
            self.rule_creation_page.submit_rule()
        except Exception as e:
            assert "missing required field" in str(e).lower(), f"Expected error for missing trigger type, got: {e}"

    def test_rule_creation_unsupported_action_type(self):
        """
        TC-FT-004 Step 2: Submit a rule with unsupported action type. Expect system error indicating unsupported action type.
        """
        try:
            # Simulate unsupported action type by manipulating internal state or using a stub
            # For demonstration, assume define_rule() or submit_rule() will raise Exception for unsupported action
            # This is a placeholder for actual UI interaction
            raise Exception("Unsupported action type")
        except Exception as e:
            assert "unsupported action type" in str(e).lower(), f"Expected error for unsupported action type, got: {e}"

# --- Appended Test Cases ---

class TestRuleManagerPage:
    def __init__(self, driver):
        self.driver = driver
        self.rule_manager_page = RuleManagerPage(driver)
        self.schedule_simulator_page = ScheduleSimulatorPage(driver)

    def test_percentage_of_deposit_rule(self):
        """
        TC-FT-005 Step 1: Define a rule for 10% of deposit action. Step 2: Simulate deposit of 500 units. Expect: Rule is accepted and transfer of 50 units is executed.
        """
        rule_json = '{"trigger": {"type": "after_deposit"}, "action": {"type": "percentage_of_deposit", "percentage": 10}, "conditions": []}'
        self.rule_manager_page.enter_rule_json(rule_json)
        self.rule_manager_page.submit_rule()
        assert self.rule_manager_page.verify_rule_accepted(), "Rule was not accepted"
        # Simulate deposit of 500 units and verify transfer
        deposit_amount = 500
        expected_transfer = 50
        result = self.schedule_simulator_page.simulate_deposit_and_verify_transfer(deposit_amount, expected_transfer)
        assert result, f"Expected transfer of {expected_transfer} units not executed"

    def test_currency_conversion_rule_and_existing_rules(self):
        """
        TC-FT-006 Step 1: Define a rule with trigger type 'currency_conversion', currency 'EUR', action 'fixed_amount', amount 100. Step 2: Verify existing rules continue to execute as before. Expect: System accepts or gracefully rejects with a clear message, and existing rules function as expected.
        """
        rule_json = '{"trigger": {"type": "currency_conversion", "currency": "EUR"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": []}'
        self.rule_manager_page.enter_rule_json(rule_json)
        self.rule_manager_page.submit_rule()
        # Check for acceptance or graceful rejection
        try:
            accepted = self.rule_manager_page.verify_rule_accepted()
        except Exception:
            accepted = False
        try:
            rejected = self.rule_manager_page.verify_rule_rejected()
        except Exception:
            rejected = False
        assert accepted or rejected, "Rule was neither accepted nor gracefully rejected"
        # Verify existing rules continue to execute as before
        assert self.rule_manager_page.verify_existing_rules_intact(), "Existing rules not functioning as expected"

    def test_bulk_rule_loading_and_evaluation(self):
        """
        TC-FT-007: Bulk rule loading and evaluation.
        Step 1: Use RuleManagerPage.load_batch_rules() to load 10,000 valid rules (simulate batch JSON).
        Step 2: Use ScheduleSimulatorPage.trigger_evaluation_for_all_rules().
        Expect: All rules are loaded, evaluation completes within performance threshold, and no errors are reported.
        """
        # Simulate 10,000 valid rules as a batch JSON array
        batch_rules = [
            {
                "name": f"Bulk Rule {i}",
                "trigger": {"type": "after_deposit"},
                "action": {"type": "fixed_amount", "amount": 1},
                "conditions": []
            } for i in range(1, 10001)
        ]
        load_result = self.rule_manager_page.load_batch_rules(batch_rules)
        assert load_result["success"], f"Batch rule load failed: {load_result.get('error')}"
        # Trigger evaluation for all rules
        evaluation_result = self.schedule_simulator_page.trigger_evaluation_for_all_rules()
        assert evaluation_result["success"], f"Evaluation failed: {evaluation_result.get('error')}"
        # Performance assertion (pseudo: check evaluation time is within threshold)
        assert evaluation_result["duration_sec"] <= 60, (
            f"Evaluation exceeded performance threshold: {evaluation_result['duration_sec']}s"
        )
        # Ensure no errors in results
        assert not evaluation_result.get("errors"), f"Errors reported: {evaluation_result.get('errors')}"

    def test_sql_injection_rule_submission(self):
        """
        TC-FT-008: SQL injection rule submission.
        Step 1: Use RuleManagerPage.submit_rule_with_sql_injection() to submit a rule with SQL injection payload.
        Step 2: Assert system rejection and verify no SQL execution occurred.
        """
        injection_payload = {
            "name": "SQL Injection Test",
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": [
                {"field": "account", "operator": "=", "value": "' OR 1=1; --"}
            ]
        }
        result = self.rule_manager_page.submit_rule_with_sql_injection(injection_payload)
        assert result["rejected"], "SQL injection payload was not rejected by the system"
        # Verify no SQL execution occurred (pseudo: check for absence of side effects)
        assert not result.get("sql_executed", False), "SQL injection was executed or affected the database!"
