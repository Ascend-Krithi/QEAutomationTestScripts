from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object for Rule Configuration Page.
    Handles rule creation, trigger setup (specific_date, recurring, after_deposit, currency_conversion),
    action setup (fixed_amount and percentage_of_deposit), conditions, validation,
    system time simulation, deposit simulation, and transfer action validation.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators from Locators.json
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

    def open_rule_form(self):
        self.wait.until(EC.visibility_of_element_located(self.locators['ruleIdInput']))

    def set_rule_id(self, rule_id):
        rule_id_input = self.wait.until(EC.visibility_of_element_located(self.locators['ruleIdInput']))
        rule_id_input.clear()
        rule_id_input.send_keys(rule_id)

    def set_rule_name(self, rule_name):
        rule_name_input = self.wait.until(EC.visibility_of_element_located(self.locators['ruleNameInput']))
        rule_name_input.clear()
        rule_name_input.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.locators['triggerTypeDropdown']))
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='trigger-type-select']/option[@value='{trigger_type}']")
        option.click()

    def set_specific_date_trigger(self, date_str):
        self.select_trigger_type('specific_date')
        date_input = self.wait.until(EC.visibility_of_element_located(self.locators['datePicker']))
        date_input.clear()
        date_input.send_keys(date_str)

    def set_recurring_trigger(self, interval):
        self.select_trigger_type('recurring')
        interval_input = self.wait.until(EC.visibility_of_element_located(self.locators['recurringIntervalInput']))
        interval_input.clear()
        interval_input.send_keys(interval)

    def set_after_deposit_trigger(self):
        """
        Sets the after_deposit trigger toggle.
        """
        self.select_trigger_type('after_deposit')
        toggle = self.wait.until(EC.element_to_be_clickable(self.locators['afterDepositToggle']))
        if not toggle.is_selected():
            toggle.click()

    def set_currency_conversion_trigger(self, currency):
        """
        Sets the currency_conversion trigger type if supported, else returns error message.
        """
        try:
            self.select_trigger_type('currency_conversion')
            # If UI provides currency dropdown/input, set it
            currency_input = self.driver.find_element(By.XPATH, f"//input[@name='currency']")
            currency_input.clear()
            currency_input.send_keys(currency)
            return True
        except Exception as e:
            return f"Currency conversion trigger type not supported: {str(e)}"

    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.locators['actionTypeDropdown']))
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='action-type-select']/option[@value='{action_type}']")
        option.click()

    def set_fixed_amount_action(self, amount):
        self.select_action_type('fixed_amount')
        amount_input = self.wait.until(EC.visibility_of_element_located(self.locators['transferAmountInput']))
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_percentage_of_deposit_action(self, percentage):
        self.select_action_type('percentage_of_deposit')
        percentage_input = self.wait.until(EC.visibility_of_element_located(self.locators['percentageInput']))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        dest_input = self.wait.until(EC.visibility_of_element_located(self.locators['destinationAccountInput']))
        dest_input.clear()
        dest_input.send_keys(account_id)

    def add_condition(self, condition):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.locators['addConditionBtn']))
        add_btn.click()
        # Assume condition is a dict with type, operator, value
        type_dropdown = self.wait.until(EC.element_to_be_clickable(self.locators['conditionTypeDropdown']))
        type_dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[contains(@class,'condition-type')]/option[@value='{condition.get('type','')}']")
        option.click()
        operator_dropdown = self.wait.until(EC.element_to_be_clickable(self.locators['operatorDropdown']))
        operator_dropdown.click()
        op_option = self.driver.find_element(By.XPATH, f"//select[contains(@class,'condition-operator-select')]/option[@value='{condition.get('operator','')}']")
        op_option.click()
        if 'balanceThreshold' in condition:
            balance_input = self.wait.until(EC.visibility_of_element_located(self.locators['balanceThresholdInput']))
            balance_input.clear()
            balance_input.send_keys(str(condition['balanceThreshold']))
        if 'transactionSource' in condition:
            source_dropdown = self.wait.until(EC.element_to_be_clickable(self.locators['transactionSourceDropdown']))
            source_dropdown.click()
            source_option = self.driver.find_element(By.XPATH, f"//select[@id='source-provider-select']/option[@value='{condition['transactionSource']}']")
            source_option.click()

    def enter_json_schema(self, rule_json):
        editor = self.wait.until(EC.visibility_of_element_located(self.locators['jsonSchemaEditor']))
        editor.clear()
        editor.send_keys(rule_json)

    def validate_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.locators['validateSchemaBtn']))
        validate_btn.click()
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.locators['successMessage']))
            return msg.text
        except:
            err = self.wait.until(EC.visibility_of_element_located(self.locators['schemaErrorMessage']))
            return err.text

    def save_rule(self):
        save_btn = self.wait.until(EC.element_to_be_clickable(self.locators['saveRuleButton']))
        save_btn.click()

    def create_rule(self, rule_json):
        """
        Orchestrates rule creation from JSON.
        Supports specific_date, recurring, after_deposit, and currency_conversion triggers.
        """
        self.open_rule_form()
        if 'ruleId' in rule_json:
            self.set_rule_id(rule_json['ruleId'])
        if 'ruleName' in rule_json:
            self.set_rule_name(rule_json['ruleName'])
        trigger = rule_json.get('trigger', {})
        action = rule_json.get('action', {})
        conditions = rule_json.get('conditions', [])
        # Trigger setup
        trigger_type = trigger.get('type')
        if trigger_type == 'specific_date':
            self.set_specific_date_trigger(trigger.get('date', ''))
        elif trigger_type == 'recurring':
            self.set_recurring_trigger(trigger.get('interval', ''))
        elif trigger_type == 'after_deposit':
            self.set_after_deposit_trigger()
        elif trigger_type == 'currency_conversion':
            result = self.set_currency_conversion_trigger(trigger.get('currency', ''))
            if result is not True:
                return result
        else:
            return f"Unknown trigger type: {trigger_type}"
        # Action setup
        if action.get('type') == 'fixed_amount':
            self.set_fixed_amount_action(action.get('amount', ''))
        elif action.get('type') == 'percentage_of_deposit':
            self.set_percentage_of_deposit_action(action.get('percentage', ''))
        if 'destinationAccount' in action:
            self.set_destination_account(action['destinationAccount'])
        # Conditions
        for cond in conditions:
            self.add_condition(cond)
        self.save_rule()
        return self.validate_schema()

    def simulate_deposit(self, amount):
        """
        Simulates deposit action for testing.
        This implementation assumes there is a test-only UI element or API endpoint exposed.
        """
        # Example: Locate deposit input and submit button if available
        try:
            deposit_input = self.driver.find_element(By.XPATH, "//input[@name='deposit-amount']")
            deposit_input.clear()
            deposit_input.send_keys(str(amount))
            submit_btn = self.driver.find_element(By.XPATH, "//button[@data-testid='submit-deposit']")
            submit_btn.click()
            # Wait for confirmation
            confirmation = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))
            return confirmation.text
        except Exception as e:
            return f"Deposit simulation not supported: {str(e)}"

    def validate_transfer_action(self, expected_amount=None, expected_percentage=None, expected_count=1):
        """
        Validates that transfer action was executed as expected.
        This implementation assumes there is an audit trail, notification, or transaction log UI or API.
        """
        # Example: Check transaction log for matching entry
        # Placeholder: raise NotImplementedError if not supported
        raise NotImplementedError("Transfer action validation must be implemented in test environment.")

    def verify_existing_rules(self):
        """
        Verifies that existing rules are not affected by new rule creation.
        This implementation assumes there is a rules list UI or API.
        """
        # Example: Fetch rules and validate their state
        try:
            rules_list = self.driver.find_elements(By.CSS_SELECTOR, '.rule-list-item')
            return [rule.text for rule in rules_list]
        except Exception as e:
            return f"Could not verify existing rules: {str(e)}"
