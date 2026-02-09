# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            'ruleIdInput': (By.ID, 'rule-id-field'),
            'ruleNameInput': (By.NAME, 'rule-name'),
            'saveRuleButton': (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']"),
            'triggerTypeDropdown': (By.ID, 'trigger-type-select'),
            'datePicker': (By.CSS_SELECTOR, "input[type='date']"),
            'recurringIntervalInput': (By.ID, 'interval-value'),
            'afterDepositToggle': (By.ID, 'trigger-after-deposit'),
            'addConditionBtn': (By.ID, 'add-condition-link'),
            'conditionTypeDropdown': (By.CSS_SELECTOR, 'select.condition-type'),
            'balanceThresholdInput': (By.CSS_SELECTOR, "input[name='balance-limit']"),
            'transactionSourceDropdown': (By.ID, 'source-provider-select'),
            'operatorDropdown': (By.CSS_SELECTOR, '.condition-operator-select'),
            'actionTypeDropdown': (By.ID, 'action-type-select'),
            'transferAmountInput': (By.NAME, 'fixed-amount'),
            'percentageInput': (By.ID, 'deposit-percentage'),
            'destinationAccountInput': (By.ID, 'target-account-id'),
            'jsonSchemaEditor': (By.CSS_SELECTOR, '.monaco-editor'),
            'validateSchemaBtn': (By.ID, 'btn-verify-json'),
            'successMessage': (By.CSS_SELECTOR, '.alert-success'),
            'schemaErrorMessage': (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
        }

    def enter_rule_id(self, rule_id):
        elem = self.driver.find_element(*self.locators['ruleIdInput'])
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        elem = self.driver.find_element(*self.locators['ruleNameInput'])
        elem.clear()
        elem.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.driver.find_element(*self.locators['triggerTypeDropdown'])
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text.lower() == trigger_type.lower():
                option.click()
                break

    def add_condition(self, condition_type, operator, value):
        self.driver.find_element(*self.locators['addConditionBtn']).click()
        cond_type_dropdown = self.driver.find_element(*self.locators['conditionTypeDropdown'])
        for option in cond_type_dropdown.find_elements_by_tag_name('option'):
            if option.text.lower() == condition_type.lower():
                option.click()
                break
        operator_dropdown = self.driver.find_element(*self.locators['operatorDropdown'])
        for option in operator_dropdown.find_elements_by_tag_name('option'):
            if option.text == operator:
                option.click()
                break
        value_input = self.driver.find_element(*self.locators['balanceThresholdInput'])
        value_input.clear()
        value_input.send_keys(str(value))

    def add_action(self, action_type, account, amount):
        action_type_dropdown = self.driver.find_element(*self.locators['actionTypeDropdown'])
        for option in action_type_dropdown.find_elements_by_tag_name('option'):
            if option.text.lower() == action_type.lower():
                option.click()
                break
        dest_account_input = self.driver.find_element(*self.locators['destinationAccountInput'])
        dest_account_input.clear()
        dest_account_input.send_keys(account)
        amount_input = self.driver.find_element(*self.locators['transferAmountInput'])
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def enter_json_schema(self, schema_str):
        # Assumes Monaco Editor is accessible via JS execution
        editor = self.driver.find_element(*self.locators['jsonSchemaEditor'])
        self.driver.execute_script("arguments[0].innerText = arguments[1]", editor, schema_str)

    def validate_schema(self):
        self.driver.find_element(*self.locators['validateSchemaBtn']).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.locators['successMessage'])
        )

    def get_success_message(self):
        return self.driver.find_element(*self.locators['successMessage']).text

    def get_schema_error_message(self):
        return self.driver.find_element(*self.locators['schemaErrorMessage']).text

    # --- TEST CASE TC_SCRUM158_07 ---
    def create_rule_with_required_fields(self, rule_id, rule_name, schema_dict):
        """
        Implements Test Case TC_SCRUM158_07:
        - Prepare a schema with only required fields (one trigger, one condition, one action).
        - Submit the schema and verify rule creation.
        """
        import json
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.enter_json_schema(json.dumps(schema_dict))
        self.validate_schema()
        self.driver.find_element(*self.locators['saveRuleButton']).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.locators['successMessage'])
        )
        return self.get_success_message()

    # --- TEST CASE TC_SCRUM158_08 ---
    def create_rule_with_large_metadata(self, rule_id, rule_name, schema_dict):
        """
        Implements Test Case TC_SCRUM158_08:
        - Prepare a schema with a large metadata field (e.g., 10,000 characters).
        - Submit and verify rule is accepted if within limits; performance is acceptable.
        """
        import json
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.enter_json_schema(json.dumps(schema_dict))
        self.validate_schema()
        self.driver.find_element(*self.locators['saveRuleButton']).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.locators['successMessage'])
        )
        return self.get_success_message()
