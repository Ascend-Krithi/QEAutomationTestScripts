from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    def navigate_to_rule_creation(self):
        # Implementation depends on application navigation, placeholder
        pass

    def define_specific_date_trigger(self, date_str):
        self.trigger_type_dropdown.click()
        # Assume dropdown options are selectable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'trigger-type-select')))
        self.trigger_type_dropdown.send_keys('specific_date')
        self.date_picker.clear()
        self.date_picker.send_keys(date_str)

    def add_balance_threshold_condition(self, operator, amount):
        self.add_condition_btn.click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.condition-type')))
        self.condition_type_dropdown.send_keys('balance_threshold')
        self.operator_dropdown.send_keys(operator)
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(str(amount))

    def add_fixed_transfer_action(self, amount, destination_account):
        self.action_type_dropdown.click()
        self.action_type_dropdown.send_keys('fixed_transfer')
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(str(amount))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def save_rule(self):
        self.save_rule_button.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of(self.success_message))

    def retrieve_saved_rule(self, rule_id):
        # Placeholder for retrieval logic, depends on app
        pass

    def validate_schema(self):
        self.validate_schema_btn.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '.alert-success')))
