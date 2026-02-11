from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Rule Form Methods
    def enter_rule_id(self, rule_id):
        rule_id_input = self.wait.until(EC.visibility_of_element_located((By.ID, "rule-id-field")))
        rule_id_input.clear()
        rule_id_input.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        rule_name_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "rule-name")))
        rule_name_input.clear()
        rule_name_input.send_keys(rule_name)

    def save_rule(self):
        save_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")))
        save_button.click()

    # Trigger Methods
    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "trigger-type-select")))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[@id='trigger-type-select']/option[text()='{trigger_type}']")))
        option.click()

    def enter_invalid_trigger_type(self, invalid_type):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "trigger-type-select")))
        dropdown.clear()
        dropdown.send_keys(invalid_type)

    def set_date_picker(self, date_value):
        date_picker = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='date']")))
        date_picker.clear()
        date_picker.send_keys(date_value)

    def set_recurring_interval(self, interval):
        interval_input = self.wait.until(EC.visibility_of_element_located((By.ID, "interval-value")))
        interval_input.clear()
        interval_input.send_keys(interval)

    def toggle_after_deposit(self):
        toggle = self.wait.until(EC.visibility_of_element_located((By.ID, "trigger-after-deposit")))
        toggle.click()

    # Conditions Methods
    def add_condition(self):
        add_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "add-condition-link")))
        add_btn.click()

    def select_condition_type(self, condition_type):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "select.condition-type")))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[contains(@class, 'condition-type')]/option[text()='{condition_type}']")))
        option.click()

    def enter_balance_threshold(self, threshold):
        input_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='balance-limit'")))
        input_field.clear()
        input_field.send_keys(threshold)

    def select_transaction_source(self, source):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "source-provider-select")))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[@id='source-provider-select']/option[text()='{source}']")))
        option.click()

    def select_operator(self, operator):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".condition-operator-select")))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[contains(@class, 'condition-operator-select')]/option[text()='{operator}']")))
        option.click()

    # Actions Methods
    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "action-type-select")))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//select[@id='action-type-select']/option[text()='{action_type}']")))
        option.click()

    def enter_transfer_amount(self, amount):
        input_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "fixed-amount")))
        input_field.clear()
        input_field.send_keys(amount)

    def enter_percentage(self, percentage):
        input_field = self.wait.until(EC.visibility_of_element_located((By.ID, "deposit-percentage")))
        input_field.clear()
        input_field.send_keys(percentage)

    def enter_destination_account(self, account_id):
        input_field = self.wait.until(EC.visibility_of_element_located((By.ID, "target-account-id")))
        input_field.clear()
        input_field.send_keys(account_id)

    # Validation Methods
    def edit_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".monaco-editor")))
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-verify-json")))
        validate_btn.click()

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))).text

    def get_schema_error_message(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='error-feedback-text']"))).text

    # Utility Methods for Required Field Testing
    def clear_rule_form_fields(self):
        self.enter_rule_id("")
        self.enter_rule_name("")
