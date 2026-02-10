from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Rule Form ---
    def enter_rule_id(self, rule_id):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, 'rule-id-field')))
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        elem = self.wait.until(EC.visibility_of_element_located((By.NAME, 'rule-name')))
        elem.clear()
        elem.send_keys(rule_name)

    def click_save_rule(self):
        elem = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")))
        elem.click()

    # --- Triggers ---
    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, 'trigger-type-select')))
        dropdown.click()
        dropdown.send_keys(trigger_type)
        dropdown.send_keys(Keys.RETURN)

    def set_date_picker(self, date_str):
        elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='date']")))
        elem.clear()
        elem.send_keys(date_str)

    def set_recurring_interval(self, interval):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, 'interval-value')))
        elem.clear()
        elem.send_keys(str(interval))

    def toggle_after_deposit(self):
        toggle = self.wait.until(EC.element_to_be_clickable((By.ID, 'trigger-after-deposit')))
        toggle.click()

    # --- Conditions ---
    def click_add_condition(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'add-condition-link')))
        btn.click()

    def select_condition_type(self, condition_type):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select.condition-type')))
        dropdown.click()
        dropdown.send_keys(condition_type)
        dropdown.send_keys(Keys.RETURN)

    def enter_balance_threshold(self, threshold):
        elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='balance-limit']")))
        elem.clear()
        elem.send_keys(str(threshold))

    def select_transaction_source(self, source):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, 'source-provider-select')))
        dropdown.click()
        dropdown.send_keys(source)
        dropdown.send_keys(Keys.RETURN)

    def select_operator(self, operator):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.condition-operator-select')))
        dropdown.click()
        dropdown.send_keys(operator)
        dropdown.send_keys(Keys.RETURN)

    # --- Actions ---
    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, 'action-type-select')))
        dropdown.click()
        dropdown.send_keys(action_type)
        dropdown.send_keys(Keys.RETURN)

    def enter_transfer_amount(self, amount):
        elem = self.wait.until(EC.visibility_of_element_located((By.NAME, 'fixed-amount')))
        elem.clear()
        elem.send_keys(str(amount))

    def enter_percentage(self, percentage):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, 'deposit-percentage')))
        elem.clear()
        elem.send_keys(str(percentage))

    def enter_destination_account(self, account_id):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, 'target-account-id')))
        elem.clear()
        elem.send_keys(account_id)

    # --- Validation ---
    def enter_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.monaco-editor')))
        editor.click()
        editor.send_keys(schema_text)

    def click_validate_schema(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'btn-verify-json')))
        btn.click()

    def get_success_message(self):
        msg = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))
        return msg.text

    def get_schema_error_message(self):
        msg = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='error-feedback-text']")))
        return msg.text
