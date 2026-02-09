# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
import json

class RuleConfigurationPage:
    """
    Page Object for Rule Configuration Page.
    Covers: triggers, conditions, actions, validation, and rule form.
    Locators loaded from Locators.json.
    """

    def __init__(self, driver: WebDriver, locators: dict):
        self.driver = driver
        self.locators = locators["RuleConfigurationPage"]

    # --- Rule Form ---
    def enter_rule_id(self, rule_id: str):
        elem = self.driver.find_element(By.ID, self.locators["ruleForm"]["ruleIdInput"].split('=')[1])
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name: str):
        elem = self.driver.find_element(By.NAME, self.locators["ruleForm"]["ruleNameInput"].split('=')[1])
        elem.clear()
        elem.send_keys(rule_name)

    def click_save_rule(self):
        elem = self.driver.find_element(By.CSS_SELECTOR, self.locators["ruleForm"]["saveRuleButton"])
        elem.click()

    # --- Triggers ---
    def select_trigger_type(self, trigger_type: str):
        dropdown = self.driver.find_element(By.ID, self.locators["triggers"]["triggerTypeDropdown"].split('=')[1])
        dropdown.click()
        # Add logic to select trigger_type from dropdown

    def set_date_picker(self, date_str: str):
        date_input = self.driver.find_element(By.CSS_SELECTOR, self.locators["triggers"]["datePicker"])
        date_input.clear()
        date_input.send_keys(date_str)

    def set_recurring_interval(self, interval: str):
        interval_input = self.driver.find_element(By.ID, self.locators["triggers"]["recurringIntervalInput"].split('=')[1])
        interval_input.clear()
        interval_input.send_keys(interval)

    def toggle_after_deposit(self, enable: bool):
        toggle = self.driver.find_element(By.ID, self.locators["triggers"]["afterDepositToggle"].split('=')[1])
        if toggle.is_selected() != enable:
            toggle.click()

    # --- Conditions ---
    def click_add_condition(self):
        btn = self.driver.find_element(By.ID, self.locators["conditions"]["addConditionBtn"].split('=')[1])
        btn.click()

    def select_condition_type(self, condition_type: str):
        dropdown = self.driver.find_element(By.CSS_SELECTOR, self.locators["conditions"]["conditionTypeDropdown"])
        dropdown.click()
        # Add logic to select condition_type

    def enter_balance_threshold(self, threshold: str):
        input_elem = self.driver.find_element(By.CSS_SELECTOR, self.locators["conditions"]["balanceThresholdInput"])
        input_elem.clear()
        input_elem.send_keys(threshold)

    def select_transaction_source(self, source: str):
        dropdown = self.driver.find_element(By.ID, self.locators["conditions"]["transactionSourceDropdown"].split('=')[1])
        dropdown.click()
        # Add logic to select source

    def select_operator(self, operator: str):
        dropdown = self.driver.find_element(By.CSS_SELECTOR, self.locators["conditions"]["operatorDropdown"])
        dropdown.click()
        # Add logic to select operator

    # --- Actions ---
    def select_action_type(self, action_type: str):
        dropdown = self.driver.find_element(By.ID, self.locators["actions"]["actionTypeDropdown"].split('=')[1])
        dropdown.click()
        # Add logic to select action_type

    def enter_transfer_amount(self, amount: str):
        input_elem = self.driver.find_element(By.NAME, self.locators["actions"]["transferAmountInput"].split('=')[1])
        input_elem.clear()
        input_elem.send_keys(amount)

    def enter_percentage(self, percentage: str):
        input_elem = self.driver.find_element(By.ID, self.locators["actions"]["percentageInput"].split('=')[1])
        input_elem.clear()
        input_elem.send_keys(percentage)

    def enter_destination_account(self, account_id: str):
        input_elem = self.driver.find_element(By.ID, self.locators["actions"]["destinationAccountInput"].split('=')[1])
        input_elem.clear()
        input_elem.send_keys(account_id)

    # --- Validation ---
    def edit_json_schema(self, schema: dict):
        editor = self.driver.find_element(By.CSS_SELECTOR, self.locators["validation"]["jsonSchemaEditor"])
        editor.clear()
        editor.send_keys(json.dumps(schema))

    def click_validate_schema(self):
        btn = self.driver.find_element(By.ID, self.locators["validation"]["validateSchemaBtn"].split('=')[1])
        btn.click()

    def get_success_message(self):
        try:
            msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators["validation"]["successMessage"]))
            )
            return msg.text
        except TimeoutException:
            return None

    def get_schema_error_message(self):
        try:
            msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators["validation"]["schemaErrorMessage"]))
            )
            return msg.text
        except TimeoutException:
            return None
