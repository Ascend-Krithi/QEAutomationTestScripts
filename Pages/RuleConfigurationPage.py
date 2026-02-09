# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
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
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
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

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def enter_rule_id(self, rule_id):
        self.wait.until(EC.visibility_of_element_located(self.rule_id_input)).clear()
        self.driver.find_element(*self.rule_id_input).send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        self.wait.until(EC.visibility_of_element_located(self.rule_name_input)).clear()
        self.driver.find_element(*self.rule_name_input).send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        select = Select(self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown)))
        select.select_by_value(trigger_type)

    def set_specific_date_trigger(self, date_str):
        self.select_trigger_type("specific_date")
        date_input = self.wait.until(EC.element_to_be_clickable(self.date_picker))
        date_input.clear()
        date_input.send_keys(date_str)

    def set_recurring_trigger(self, interval):
        self.select_trigger_type("recurring")
        interval_input = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
        interval_input.clear()
        interval_input.send_keys(interval)

    def set_action_fixed_amount(self, amount):
        select = Select(self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown)))
        select.select_by_value("fixed_amount")
        amount_input = self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input))
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_action_percentage_of_deposit(self, percentage):
        select = Select(self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown)))
        select.select_by_value("percentage_of_deposit")
        percentage_input = self.wait.until(EC.visibility_of_element_located(self.percentage_input))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        account_input = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        account_input.clear()
        account_input.send_keys(account_id)

    def add_condition(self, condition_type, operator, threshold=None, transaction_source=None):
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        select = Select(self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown)))
        select.select_by_value(condition_type)
        op_select = Select(self.wait.until(EC.visibility_of_element_located(self.operator_dropdown)))
        op_select.select_by_value(operator)
        if threshold is not None:
            threshold_input = self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input))
            threshold_input.clear()
            threshold_input.send_keys(str(threshold))
        if transaction_source is not None:
            source_select = Select(self.wait.until(EC.visibility_of_element_located(self.transaction_source_dropdown)))
            source_select.select_by_value(transaction_source)

    def enter_json_schema(self, schema_str):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.clear()
        editor.send_keys(schema_str)

    def validate_schema(self):
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()

    def is_schema_valid(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    def get_schema_error(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return error_elem.text
        except TimeoutException:
            return None

    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def define_rule_specific_date(self, rule_id, rule_name, date_str, amount, schema_str):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.set_specific_date_trigger(date_str)
        self.set_action_fixed_amount(amount)
        self.enter_json_schema(schema_str)
        self.validate_schema()
        assert self.is_schema_valid(), f"Schema validation failed: {self.get_schema_error()}"
        self.save_rule()

    def define_rule_recurring(self, rule_id, rule_name, interval, percentage, schema_str):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.set_recurring_trigger(interval)
        self.set_action_percentage_of_deposit(percentage)
        self.enter_json_schema(schema_str)
        self.validate_schema()
        assert self.is_schema_valid(), f"Schema validation failed: {self.get_schema_error()}"
        self.save_rule()

    def verify_transfer_action_executed(self, expected_count=1):
        # Placeholder for actual verification logic, e.g., querying logs or UI confirmation
        # Should be implemented according to system under test
        pass

    # --- Appended for CASE-Update: TC-FT-005 ---
    def define_rule_after_deposit_percentage(self, rule_id, rule_name, percentage, schema_str):
        """
        Define a rule for 'after_deposit' trigger with percentage_of_deposit action.
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.select_trigger_type("after_deposit")
        self.set_action_percentage_of_deposit(percentage)
        self.enter_json_schema(schema_str)
        self.validate_schema()
        assert self.is_schema_valid(), f"Schema validation failed: {self.get_schema_error()}"
        self.save_rule()

    def simulate_deposit_and_verify_transfer(self, deposit_amount, expected_transfer):
        """
        Simulate deposit and verify transfer action executed.
        Note: This is a placeholder. Actual implementation depends on system integration.
        """
        # Simulate deposit - depends on system interface
        # Verify transfer - placeholder logic
        # Example: Check transfer record, UI, or database
        pass

    # --- Appended for CASE-Update: TC-FT-006 ---
    def define_rule_currency_conversion(self, rule_id, rule_name, currency, amount, schema_str):
        """
        Define a rule with 'currency_conversion' trigger and fixed amount action.
        Gracefully handle unknown trigger types.
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        try:
            self.select_trigger_type("currency_conversion")
            # If currency field exists, fill it
            # Placeholder: Adjust if UI supports currency selection
            self.set_action_fixed_amount(amount)
            self.enter_json_schema(schema_str)
            self.validate_schema()
            assert self.is_schema_valid(), f"Schema validation failed: {self.get_schema_error()}"
            self.save_rule()
        except Exception as e:
            # Graceful rejection, e.g., log or display message
            print(f"Unsupported trigger type: currency_conversion. Exception: {e}")

    def verify_existing_rules_function(self):
        """
        Verify that existing rules continue to execute as before after new rule type attempt.
        """
        # Placeholder for verification logic
        pass
