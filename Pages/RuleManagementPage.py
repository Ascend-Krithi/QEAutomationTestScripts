from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagementPage:
    def __init__(self, driver):
        self.driver = driver

    def create_rule(self, conditions, actions):
        # Example: conditions = {'balance': '>=1000', 'source': 'salary'}
        # actions = {'transfer': 'execute'}
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

    # --- Appended Methods for TC-FT-003 ---
    def add_multiple_conditions(self, conditions):
        """
        Add multiple conditions to a rule.
        conditions: dict, e.g. {'balance': '>=1000', 'source': 'salary', 'account_type': 'checking'}
        """
        for cond_key, cond_value in conditions.items():
            field = self.driver.find_element(By.ID, f"condition-{cond_key}")
            field.clear()
            field.send_keys(cond_value)

    def simulate_deposits(self, deposit_list):
        """
        Simulate multiple deposits.
        deposit_list: list of dicts, e.g. [{'amount': 500, 'source': 'salary'}, {'amount': 2000, 'source': 'bonus'}]
        """
        for deposit in deposit_list:
            self.simulate_deposit(deposit['amount'], deposit['source'])

    def validate_transfer_not_executed(self):
        """
        Validate that transfer was NOT executed (negative case).
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "transfer-success-msg"))
            )
            actual = True
        except:
            actual = False
        assert not actual, "Transfer was executed when it should NOT have been."

    # --- Appended Methods for TC-FT-004 ---
    def submit_rule_missing_trigger_type(self, actions):
        """
        Submit a rule with missing trigger type.
        actions: dict, e.g. {'transfer': 'execute'}
        """
        self.driver.find_element(By.ID, "add-rule-btn").click()
        # Do NOT fill trigger-type
        for action_key, action_value in actions.items():
            self.driver.find_element(By.ID, f"action-{action_key}").send_keys(action_value)
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def submit_rule_unsupported_action_type(self, trigger_type, unsupported_action):
        """
        Submit a rule with unsupported action type.
        trigger_type: str
        unsupported_action: dict, e.g. {'action_type': 'unsupported'}
        """
        self.driver.find_element(By.ID, "add-rule-btn").click()
        self.driver.find_element(By.ID, "trigger-type").send_keys(trigger_type)
        for action_key, action_value in unsupported_action.items():
            self.driver.find_element(By.ID, f"action-{action_key}").send_keys(action_value)
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def get_error_messages(self):
        """
        Returns all error messages shown on the page.
        """
        error_elements = self.driver.find_elements(By.CLASS_NAME, "error-msg")
        return [elem.text for elem in error_elements]

