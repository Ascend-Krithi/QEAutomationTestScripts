from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Rule Form Locators
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

        # Triggers Locators
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')

        # Conditions Locators
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')

        # Actions Locators
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')

        # Validation Locators
        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    # Rule Form Methods
    def enter_rule_id(self, rule_id):
        rule_id_elem = self.wait.until(EC.visibility_of_element_located(self.rule_id_input))
        rule_id_elem.clear()
        rule_id_elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        rule_name_elem = self.wait.until(EC.visibility_of_element_located(self.rule_name_input))
        rule_name_elem.clear()
        rule_name_elem.send_keys(rule_name)

    def save_rule(self):
        save_btn = self.wait.until(EC.element_to_be_clickable(self.save_rule_button))
        save_btn.click()

    # Trigger Methods
    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.visibility_of_element_located(self.trigger_type_dropdown))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[@id='trigger-type-select']/option[@value='{trigger_type}']")))
        option.click()

    def set_specific_date_trigger(self, date_str):
        self.select_trigger_type('specific_date')
        date_picker = self.wait.until(EC.visibility_of_element_located(self.date_picker))
        date_picker.clear()
        date_picker.send_keys(date_str)

    def set_recurring_trigger(self, interval):
        self.select_trigger_type('recurring')
        interval_input = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
        interval_input.clear()
        interval_input.send_keys(interval)

    def toggle_after_deposit(self, enable=True):
        toggle = self.wait.until(EC.element_to_be_clickable(self.after_deposit_toggle))
        if toggle.is_selected() != enable:
            toggle.click()

    # Condition Methods
    def add_condition(self, condition_type, balance_threshold=None, transaction_source=None, operator=None):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.add_condition_btn))
        add_btn.click()
        dropdown = self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[contains(@class,'condition-type')]/option[@value='{condition_type}']")))
        option.click()
        if balance_threshold is not None:
            threshold_input = self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input))
            threshold_input.clear()
            threshold_input.send_keys(str(balance_threshold))
        if transaction_source is not None:
            source_dropdown = self.wait.until(EC.visibility_of_element_located(self.transaction_source_dropdown))
            source_dropdown.click()
            source_option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[@id='source-provider-select']/option[@value='{transaction_source}']")))
            source_option.click()
        if operator is not None:
            operator_dropdown = self.wait.until(EC.visibility_of_element_located(self.operator_dropdown))
            operator_dropdown.click()
            operator_option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[contains(@class,'condition-operator-select')]/option[@value='{operator}']")))
            operator_option.click()

    # Action Methods
    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.visibility_of_element_located(self.action_type_dropdown))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[@id='action-type-select']/option[@value='{action_type}']")))
        option.click()

    def set_fixed_amount_action(self, amount, destination_account):
        self.select_action_type('fixed_amount')
        amount_input = self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input))
        amount_input.clear()
        amount_input.send_keys(str(amount))
        dest_input = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        dest_input.clear()
        dest_input.send_keys(destination_account)

    def set_percentage_action(self, percentage, destination_account):
        self.select_action_type('percentage_of_deposit')
        percentage_input = self.wait.until(EC.visibility_of_element_located(self.percentage_input))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))
        dest_input = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        dest_input.clear()
        dest_input.send_keys(destination_account)

    # Validation Methods
    def enter_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn))
        validate_btn.click()

    def get_success_message(self):
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return msg.text
        except:
            return None

    def get_schema_error_message(self):
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return msg.text
        except:
            return None

    # High-level workflow for TestCase TC-FT-001
    def define_specific_date_rule(self, rule_id, rule_name, date_str, amount, dest_account):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.set_specific_date_trigger(date_str)
        self.set_fixed_amount_action(amount, dest_account)
        self.save_rule()

    # High-level workflow for TestCase TC-FT-002
    def define_recurring_rule(self, rule_id, rule_name, interval, percentage, dest_account):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.set_recurring_trigger(interval)
        self.set_percentage_action(percentage, dest_account)
        self.save_rule()

    # --- Appended for TC-FT-003 ---
    def define_rule_with_multiple_conditions(self, rule_id, rule_name, trigger_type, trigger_value, conditions, action_type, action_value, dest_account):
        """
        conditions: list of dicts, each dict with keys: condition_type, balance_threshold, transaction_source, operator
        action_type: 'fixed_amount' or 'percentage_of_deposit'
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        if trigger_type == 'specific_date':
            self.set_specific_date_trigger(trigger_value)
        elif trigger_type == 'recurring':
            self.set_recurring_trigger(trigger_value)
        elif trigger_type == 'after_deposit':
            self.toggle_after_deposit(True)
        else:
            self.select_trigger_type(trigger_type)
        for cond in conditions:
            self.add_condition(
                condition_type=cond.get('condition_type'),
                balance_threshold=cond.get('balance_threshold'),
                transaction_source=cond.get('transaction_source'),
                operator=cond.get('operator')
            )
        if action_type == 'fixed_amount':
            self.set_fixed_amount_action(action_value, dest_account)
        elif action_type == 'percentage_of_deposit':
            self.set_percentage_action(action_value, dest_account)
        else:
            self.select_action_type(action_type)
        self.save_rule()

    def simulate_deposit_and_validate_transfer(self, deposit_amount, expected_transfer_amount):
        """
        Simulate deposit and validate transfer execution.
        This method assumes the presence of deposit simulation UI and transfer validation UI.
        """
        # Example simulation: (pseudo-locators, adjust as per actual UI)
        deposit_input = self.wait.until(EC.visibility_of_element_located((By.ID, 'simulate-deposit-amount')))
        deposit_input.clear()
        deposit_input.send_keys(str(deposit_amount))
        simulate_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'simulate-deposit-btn')))
        simulate_btn.click()
        # Validate transfer
        transfer_result = self.wait.until(EC.visibility_of_element_located((By.ID, 'transfer-result-amount')))
        actual_transfer = float(transfer_result.text)
        return actual_transfer == expected_transfer_amount

    # --- Appended for TC-FT-004 ---
    def validate_missing_trigger_error(self):
        """
        Attempts to save rule without selecting trigger, expects error message.
        """
        self.save_rule()
        error_elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="trigger-error-feedback"]')))
        return error_elem.text

    def validate_unsupported_action_type_error(self, unsupported_action_type):
        """
        Attempts to select unsupported action type and expects error feedback.
        """
        self.select_action_type(unsupported_action_type)
        self.save_rule()
        error_elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="action-error-feedback"]')))
        return error_elem.text
