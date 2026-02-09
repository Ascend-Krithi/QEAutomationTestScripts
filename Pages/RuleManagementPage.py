from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagementPage:
    def __init__(self, driver):
        self.driver = driver

    def create_rule(self, conditions, actions):
        self.driver.find_element(By.ID, "add-rule-btn").click()
        for cond_key, cond_value in conditions.items():
            self.driver.find_element(By.ID, f"condition-{cond_key}").send_keys(cond_value)
        for action_key, action_value in actions.items():
            self.driver.find_element(By.ID, f"action-{action_key}").send_keys(action_value)
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def simulate_deposit(self, amount, source):
        self.driver.find_element(By.ID, "simulate-deposit-btn").click()
        self.driver.find_element(By.ID, "deposit-amount").send_keys(str(amount))
        self.driver.find_element(By.ID, "deposit-source").send_keys(source)
        self.driver.find_element(By.ID, "deposit-submit-btn").click()

    def validate_transfer_execution(self, expected):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "transfer-success-msg"))
            )
            actual = True
        except:
            actual = False
        assert actual == expected, f"Transfer execution validation failed: expected {expected}, got {actual}"

    def submit_rule_with_invalid_data(self, trigger_type, action_type):
        self.driver.find_element(By.ID, "add-rule-btn").click()
        if trigger_type:
            self.driver.find_element(By.ID, "trigger-type").send_keys(trigger_type)
        if action_type:
            self.driver.find_element(By.ID, "action-type").send_keys(action_type)
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def validate_error_messages(self, expected_errors):
        error_elements = self.driver.find_elements(By.CLASS_NAME, "error-msg")
        errors = [elem.text for elem in error_elements]
        for expected_error in expected_errors:
            assert expected_error in errors, f"Expected error '{expected_error}' not found in {errors}"

    # --- Appended Methods for TC-FT-005 ---
    def create_percentage_of_deposit_rule(self, percentage):
        """
        Create a rule for percentage_of_deposit action.
        percentage: int
        """
        self.driver.find_element(By.ID, "add-rule-btn").click()
        self.driver.find_element(By.ID, "trigger-type").send_keys("after_deposit")
        self.driver.find_element(By.ID, "action-type").send_keys("percentage_of_deposit")
        self.driver.find_element(By.ID, "action-percentage").send_keys(str(percentage))
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def simulate_and_validate_percentage_transfer(self, deposit_amount, expected_transfer):
        """
        Simulate deposit and validate percentage transfer.
        deposit_amount: int
        expected_transfer: int
        """
        self.simulate_deposit(deposit_amount, "test_source")
        # Validate transfer amount
        transfer_elem = self.driver.find_element(By.ID, "transfer-amount")
        actual_transfer = int(transfer_elem.text)
        assert actual_transfer == expected_transfer, f"Expected transfer {expected_transfer}, got {actual_transfer}"

    # --- Appended Methods for TC-FT-006 ---
    def create_currency_conversion_rule(self, currency, amount):
        """
        Create a rule with trigger type 'currency_conversion' and fixed amount.
        """
        self.driver.find_element(By.ID, "add-rule-btn").click()
        self.driver.find_element(By.ID, "trigger-type").send_keys("currency_conversion")
        self.driver.find_element(By.ID, "trigger-currency").send_keys(currency)
        self.driver.find_element(By.ID, "action-type").send_keys("fixed_amount")
        self.driver.find_element(By.ID, "action-amount").send_keys(str(amount))
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def validate_graceful_rejection(self):
        """
        Validate system gracefully rejects unsupported rule type.
        """
        error_elem = self.driver.find_element(By.ID, "rule-error-msg")
        assert "unsupported" in error_elem.text or "not recognized" in error_elem.text or "gracefully" in error_elem.text, f"Expected graceful rejection, got: {error_elem.text}"

    def validate_existing_rules_execution(self):
        """
        Validate existing rules continue to execute as before.
        """
        # For demonstration, reuse validate_transfer_execution(True)
        self.validate_transfer_execution(True)
