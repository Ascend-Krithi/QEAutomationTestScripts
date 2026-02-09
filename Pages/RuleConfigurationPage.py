# Pages/RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RuleConfigurationPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        # Locators from Locators.json
        self.locators = {
            "ruleIdInput": (By.ID, "rule-id-field"),
            "ruleNameInput": (By.NAME, "rule-name"),
            "saveRuleButton": (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']"),
            "triggerTypeDropdown": (By.ID, "trigger-type-select"),
            "datePicker": (By.CSS_SELECTOR, "input[type='date']"),
            "recurringIntervalInput": (By.ID, "interval-value"),
            "afterDepositToggle": (By.ID, "trigger-after-deposit"),
            "addConditionBtn": (By.ID, "add-condition-link"),
            "conditionTypeDropdown": (By.CSS_SELECTOR, "select.condition-type"),
            "balanceThresholdInput": (By.CSS_SELECTOR, "input[name='balance-limit']"),
            "transactionSourceDropdown": (By.ID, "source-provider-select"),
            "operatorDropdown": (By.CSS_SELECTOR, ".condition-operator-select"),
            "actionTypeDropdown": (By.ID, "action-type-select"),
            "transferAmountInput": (By.NAME, "fixed-amount"),
            "percentageInput": (By.ID, "deposit-percentage"),
            "destinationAccountInput": (By.ID, "target-account-id"),
            "jsonSchemaEditor": (By.CSS_SELECTOR, ".monaco-editor"),
            "validateSchemaBtn": (By.ID, "btn-verify-json"),
            "successMessage": (By.CSS_SELECTOR, ".alert-success"),
            "schemaErrorMessage": (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
        }

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def fill_rule_form(self, rule_id=None, rule_name=None):
        if rule_id:
            rule_id_input = self.wait_for_element(self.locators["ruleIdInput"])
            rule_id_input.clear()
            rule_id_input.send_keys(rule_id)
        if rule_name:
            rule_name_input = self.wait_for_element(self.locators["ruleNameInput"])
            rule_name_input.clear()
            rule_name_input.send_keys(rule_name)

    def select_trigger(self, trigger):
        trigger_type_dropdown = self.wait_for_element(self.locators["triggerTypeDropdown"])
        trigger_type_dropdown.click()
        supported_triggers = ["after_deposit", "specific_date", "interval", "manual"]
        if trigger["type"] == "after_deposit":
            after_deposit_toggle = self.wait_for_element(self.locators["afterDepositToggle"])
            if not after_deposit_toggle.is_selected():
                after_deposit_toggle.click()
        elif trigger["type"] == "specific_date":
            trigger_type_dropdown.send_keys("specific_date")
            date_picker = self.wait_for_element(self.locators["datePicker"])
            date_picker.clear()
            date_picker.send_keys(trigger["date"])
        elif trigger["type"] == "interval":
            trigger_type_dropdown.send_keys("interval")
            interval_input = self.wait_for_element(self.locators["recurringIntervalInput"])
            interval_input.clear()
            interval_input.send_keys(trigger.get("value", ""))
        elif trigger["type"] == "manual":
            trigger_type_dropdown.send_keys("manual")
        else:
            # Unsupported trigger type for TC_SCRUM158_05
            trigger_type_dropdown.send_keys(trigger["type"])

    def add_conditions(self, conditions):
        for condition in conditions:
            add_condition_btn = self.wait_for_element(self.locators["addConditionBtn"])
            add_condition_btn.click()
            condition_type_dropdown = self.wait_for_element(self.locators["conditionTypeDropdown"])
            condition_type_dropdown.send_keys(condition.get("type", ""))
            if condition.get("type") == "amount":
                if "value" in condition:
                    balance_input = self.wait_for_element(self.locators["balanceThresholdInput"])
                    balance_input.clear()
                    balance_input.send_keys(str(condition["value"]))
                if "operator" in condition:
                    operator_dropdown = self.wait_for_element(self.locators["operatorDropdown"])
                    operator_dropdown.send_keys(condition["operator"])
            if "source" in condition:
                source_dropdown = self.wait_for_element(self.locators["transactionSourceDropdown"])
                source_dropdown.send_keys(condition["source"])

    def select_action(self, action):
        action_type_dropdown = self.wait_for_element(self.locators["actionTypeDropdown"])
        action_type_dropdown.click()
        action_type_dropdown.send_keys(action["type"])
        if action["type"] == "transfer":
            if "account" in action:
                dest_account_input = self.wait_for_element(self.locators["destinationAccountInput"])
                dest_account_input.clear()
                dest_account_input.send_keys(action["account"])
            if "amount" in action:
                amount_input = self.wait_for_element(self.locators["transferAmountInput"])
                amount_input.clear()
                amount_input.send_keys(str(action["amount"]))
        if "destination_account" in action:
            dest_account_input = self.wait_for_element(self.locators["destinationAccountInput"])
            dest_account_input.clear()
            dest_account_input.send_keys(action["destination_account"])

    def select_actions(self, actions):
        for action in actions:
            self.select_action(action)

    def save_rule(self):
        save_rule_button = self.wait_for_element(self.locators["saveRuleButton"])
        save_rule_button.click()

    def validate_rule_acceptance(self):
        try:
            success_msg = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["successMessage"])
            )
            return True, success_msg.text
        except TimeoutException:
            try:
                error_msg = self.driver.find_element(*self.locators["schemaErrorMessage"])
                return False, error_msg.text
            except NoSuchElementException:
                return False, "Unknown error occurred."

    # --- New Methods for Test Cases ---
    def submit_rule_schema(self, rule_id, rule_name, trigger, conditions, actions):
        self.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.select_trigger(trigger)
        self.add_conditions(conditions)
        self.select_actions(actions)
        self.save_rule()
        return self.validate_rule_acceptance()

    def submit_schema_and_validate_error(self, rule_id, rule_name, trigger, conditions, actions):
        self.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.select_trigger(trigger)
        self.add_conditions(conditions)
        self.select_actions(actions)
        self.save_rule()
        # For TC_SCRUM158_05: expect error
        try:
            error_msg = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["schemaErrorMessage"])
            )
            return False, error_msg.text
        except TimeoutException:
            return False, "Expected error message not found."

    def submit_schema_and_validate_success(self, rule_id, rule_name, trigger, conditions, actions):
        self.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.select_trigger(trigger)
        self.add_conditions(conditions)
        self.select_actions(actions)
        self.save_rule()
        # For TC_SCRUM158_06: expect success
        try:
            success_msg = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["successMessage"])
            )
            return True, success_msg.text
        except TimeoutException:
            return False, "Expected success message not found."

# --- End of RuleConfigurationPage.py ---