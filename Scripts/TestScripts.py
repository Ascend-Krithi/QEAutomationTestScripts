# Import necessary modules
import pytest
from selenium.webdriver.common.by import By
from RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    # ... (existing methods remain unchanged)
    pass

class TestRuleConfiguration:
    """
    Selenium test suite for Rule Configuration scenarios:
    - Negative amount
    - Zero amount
    - Large amount precision

    Each test method is mapped to the provided test steps and uses RuleConfigurationPage functions.
    """

    def setup_method(self, method):
        """Setup for each test method."""
        try:
            self.page = RuleConfigurationPage()
            self.page.open()
        except Exception as e:
            pytest.fail(f'Setup failed: {e}')

    def teardown_method(self, method):
        """Teardown for each test method."""
        try:
            self.page.close()
        except Exception as e:
            # Log teardown failure but do not fail test
            print(f'Teardown failed: {e}')

    def test_negative_amount_rule_validation(self):
        """
        Test Case TC_SCRUM158_007 - Negative amount scenario.

        Steps:
        1. Create rule with action_type='fixed_amount', amount=-50.
        2. Submit rule for validation.
        3. Verify validation error for negative amount.

        Expected:
        - Validation service detects negative amount.
        - Schema validation fails with error 'amount must be a positive value greater than zero'.
        """
        try:
            rule_data = {
                "trigger_type": "after_deposit",
                "action_type": "fixed_amount",
                "amount": -50
            }
            self.page.create_rule(**rule_data)
            validation_result = self.page.submit_rule_for_validation()

            assert not validation_result["success"], "Validation should fail for negative amount."
            assert "amount must be a positive value greater than zero" in validation_result.get("error_message", ""), \
                "Error message for negative amount is not as expected."
        except Exception as exc:
            pytest.fail(f"Negative amount rule validation failed: {exc}")

    def test_zero_amount_rule_validation(self):
        """
        Test Case TC_SCRUM158_007 - Zero amount scenario.

        Steps:
        4. Create rule with amount=0.
        5. Submit rule with zero amount for validation.

        Expected:
        - Schema validation fails with error 'amount must be a positive value greater than zero'.
        - Rule is not created.
        """
        try:
            rule_data = {
                "trigger_type": "after_deposit",
                "action_type": "fixed_amount",
                "amount": 0
            }
            self.page.create_rule(**rule_data)
            validation_result = self.page.submit_rule_for_validation()

            assert not validation_result["success"], "Validation should fail for zero amount."
            assert "amount must be a positive value greater than zero" in validation_result.get("error_message", ""), \
                "Error message for zero amount is not as expected."
        except Exception as exc:
            pytest.fail(f"Zero amount rule validation failed: {exc}")

    def test_large_amount_precision_rule(self):
        """
        Test Case TC_SCRUM158_008 - Large amount precision scenario.

        Steps:
        1. Create rule with action_type='fixed_amount', amount=999999999.99.
        2. Submit rule for schema validation.
        3. Verify the amount is stored with correct precision in database.
        4. Trigger the rule and verify transfer execution.

        Expected:
        - Schema accepts the large amount without overflow errors.
        - Amount is stored as 999999999.99 with decimal precision maintained.
        - Large transfer amount is processed correctly, account balance limits are validated, and precision is maintained.
        """
        try:
            rule_data = {
                "trigger_type": "after_deposit",
                "action_type": "fixed_amount",
                "amount": 999999999.99
            }
            self.page.create_rule(**rule_data)
            validation_result = self.page.submit_rule_for_validation()

            assert validation_result["success"], "Validation should succeed for large amount."
            assert validation_result.get("stored_amount") == 999999999.99, \
                "Stored amount does not match expected precision."

            # Trigger the rule and verify execution
            account_balance_before = self.page.get_account_balance()
            self.page.trigger_rule()
            account_balance_after = self.page.get_account_balance()
            expected_balance = account_balance_before - rule_data["amount"]

            assert abs(account_balance_after - expected_balance) < 0.01, \
                "Account balance after transfer does not match expected precision."
        except Exception as exc:
            pytest.fail(f"Large amount precision rule test failed: {exc}")

