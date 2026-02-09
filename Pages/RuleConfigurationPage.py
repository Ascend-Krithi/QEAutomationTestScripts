# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for the Rule Configuration Page.
    Provides methods to create rules, configure triggers, actions, validate rule schemas, and handle errors.
    Updated to explicitly support minimal rule creation for TC_SCRUM158_07.
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Locators from Locators.json
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")

    add_condition_btn = (By.ID, "add-condition-link")
    condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
    balance_threshold_input = (By.NAME, "balance-limit")
    transaction_source_dropdown = (By.ID, "source-provider-select")
    operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")

    action_type_dropdown = (By.ID, "action-type-select")
    transfer_amount_input = (By.NAME, "fixed-amount")
    percentage_input = (By.ID, "deposit-percentage")
    destination_account_input = (By.ID, "target-account-id")

    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def create_rule_minimal(self, trigger, condition, action):
        """
        Creates a rule with only required fields (one trigger, one condition, one action).
        Args:
            trigger (dict): e.g. {"type": "manual"}
            condition (dict): e.g. {"type": "amount", "operator": "==", "value": 1}
            action (dict): e.g. {"type": "transfer", "account": "G", "amount": 1}
        """
        # Configure Trigger
        self.wait.until(EC.visibility_of_element_located(self.trigger_type_dropdown)).send_keys(trigger["type"])
        # Configure Condition
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown)).send_keys(condition["type"])
        self.wait.until(EC.visibility_of_element_located(self.operator_dropdown)).send_keys(condition["operator"])
        self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input)).send_keys(str(condition["value"]))
        # Configure Action
        self.wait.until(EC.visibility_of_element_located(self.action_type_dropdown)).send_keys(action["type"])
        self.wait.until(EC.visibility_of_element_located(self.destination_account_input)).send_keys(action["account"])
        self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input)).send_keys(str(action["amount"]))
        # Submit Rule
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def verify_success_message(self, expected_text):
        """
        Verifies the success message after rule submission.
        Args:
            expected_text (str): Expected message content, e.g. "Rule is created successfully."
        """
        success_elem = self.wait.until(EC.visibility_of_element_located(self.success_message))
        assert expected_text in success_elem.text, f"Expected success message '{expected_text}' not found."

    # Existing methods retained for completeness and extensibility
    def add_multiple_conditions(self, conditions):
        for cond in conditions:
            self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
            self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown)).send_keys(cond["type"])
            if "operator" in cond:
                self.wait.until(EC.visibility_of_element_located(self.operator_dropdown)).send_keys(cond["operator"])
            self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input)).send_keys(str(cond["value"]))

    def add_multiple_actions(self, actions):
        for act in actions:
            self.wait.until(EC.visibility_of_element_located(self.action_type_dropdown)).send_keys(act["type"])
            self.wait.until(EC.visibility_of_element_located(self.destination_account_input)).send_keys(act["account"])
            self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input)).send_keys(str(act["amount"]))

    def submit_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def submit_rule_with_unsupported_trigger(self, schema):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.clear()
        editor.send_keys(str(schema))
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()

    def verify_error_message(self, expected_error):
        error_elem = self.wait.until(self.wait.until(EC.visibility_of_element_located(self.schema_error_message)))
        assert expected_error in error_elem.text, f"Expected error message '{expected_error}' not found."

    def create_rule_with_max_conditions_actions(self, trigger, conditions, actions):
        self.wait.until(EC.visibility_of_element_located(self.trigger_type_dropdown)).send_keys(trigger["type"])
        self.add_multiple_conditions(conditions)
        self.add_multiple_actions(actions)
        self.submit_rule()

    def verify_rule_contains_max_items(self, expected_count):
        rule_summary = self.driver.find_element(By.ID, "rule-summary")
        assert str(expected_count) in rule_summary.text, f"Expected {expected_count} items in rule, found: {rule_summary.text}"
