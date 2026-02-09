from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

        # Locators
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')

        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')

        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')

        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    # Test Case 1: Load 10,000 valid rules and verify performance
    def load_rules_and_verify_performance(self, rules):
        import time
        start_time = time.time()
        for rule in rules:
            self.add_rule(rule['id'], rule['name'])
        end_time = time.time()
        return end_time - start_time

    def add_rule(self, rule_id, rule_name):
        self.wait.until(EC.visibility_of_element_located(self.rule_id_input)).clear()
        self.driver.find_element(*self.rule_id_input).send_keys(rule_id)
        self.wait.until(EC.visibility_of_element_located(self.rule_name_input)).clear()
        self.driver.find_element(*self.rule_name_input).send_keys(rule_name)
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    # Test Case 2: Trigger evaluation for all rules
    def trigger_evaluation_for_all_rules(self):
        self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown)).click()
        # Assuming evaluation is triggered by selecting a type and confirming
        self.driver.find_element(*self.trigger_type_dropdown).send_keys('Evaluate All')
        # Add more steps as per UI requirement

    # Test Case 3: Submit a rule with SQL injection and verify rejection
    def submit_rule_with_sql_injection(self, sql_payload):
        self.wait.until(EC.visibility_of_element_located(self.rule_id_input)).clear()
        self.driver.find_element(*self.rule_id_input).send_keys(sql_payload)
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return error.text
        except TimeoutException:
            return None

    # Utility methods for interacting with page elements
    def set_trigger(self, trigger_type, date=None, interval=None, after_deposit=False):
        self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown)).click()
        self.driver.find_element(*self.trigger_type_dropdown).send_keys(trigger_type)
        if date:
            self.driver.find_element(*self.date_picker).send_keys(date)
        if interval:
            self.driver.find_element(*self.recurring_interval_input).send_keys(interval)
        if after_deposit:
            self.driver.find_element(*self.after_deposit_toggle).click()

    def add_condition(self, condition_type, balance_threshold=None, source=None, operator=None):
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        self.driver.find_element(*self.condition_type_dropdown).send_keys(condition_type)
        if balance_threshold:
            self.driver.find_element(*self.balance_threshold_input).send_keys(balance_threshold)
        if source:
            self.driver.find_element(*self.transaction_source_dropdown).send_keys(source)
        if operator:
            self.driver.find_element(*self.operator_dropdown).send_keys(operator)

    def set_action(self, action_type, amount=None, percentage=None, destination_account=None):
        self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown)).click()
        self.driver.find_element(*self.action_type_dropdown).send_keys(action_type)
        if amount:
            self.driver.find_element(*self.transfer_amount_input).send_keys(amount)
        if percentage:
            self.driver.find_element(*self.percentage_input).send_keys(percentage)
        if destination_account:
            self.driver.find_element(*self.destination_account_input).send_keys(destination_account)

    def validate_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.clear()
        editor.send_keys(schema_text)
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return success.text
        except TimeoutException:
            try:
                error = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
                return error.text
            except TimeoutException:
                return None

    # Test Case TC_SCRUM158_09: Submit schema with malicious metadata and verify rejection
    def submit_schema_with_malicious_metadata(self, schema_text):
        '''
        Submits a schema with malicious script in metadata and verifies error message is shown.
        schema_text: JSON string containing the schema with <script> in metadata.
        Returns the error message if present.
        '''
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.clear()
        editor.send_keys(schema_text)
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return error.text
        except TimeoutException:
            return None
