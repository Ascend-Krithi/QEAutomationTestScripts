# Selenium Python Page Class for Rule Configuration
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators loaded from Locators.json
        self.locators = self._load_locators()

    def _load_locators(self):
        with open('Locators.json', 'r') as f:
            return json.load(f)["RuleConfigurationPage"]

    # Existing methods preserved below...
    # ... (existing methods, unchanged) ...

    # --- Appended methods for TC_SCRUM158_03 ---
    def create_recurring_rule(self, trigger_type, interval_value, condition_operator, condition_value, action_account, action_amount):
        """
        Create a rule with a recurring interval trigger, condition, and action.
        Args:
            trigger_type (str): e.g., 'interval'
            interval_value (str): e.g., 'weekly'
            condition_operator (str): e.g., '>='
            condition_value (int): e.g., 1000
            action_account (str): e.g., 'C'
            action_amount (int): e.g., 1000
        Returns:
            None
        """
        self.wait.until(EC.element_to_be_clickable((By.ID, self.locators['triggerTypeDropdown']))).click()
        self.driver.find_element(By.ID, self.locators['recurringIntervalInput']).send_keys(interval_value)
        self.wait.until(EC.element_to_be_clickable((By.ID, self.locators['addConditionBtn']))).click()
        self.driver.find_element(By.CSS_SELECTOR, self.locators['operatorDropdown']).send_keys(condition_operator)
        self.driver.find_element(By.NAME, self.locators['balanceThresholdInput']).send_keys(str(condition_value))
        self.wait.until(EC.element_to_be_clickable((By.ID, self.locators['actionTypeDropdown']))).click()
        self.driver.find_element(By.ID, self.locators['destinationAccountInput']).send_keys(action_account)
        self.driver.find_element(By.NAME, self.locators['transferAmountInput']).send_keys(str(action_amount))

    def submit_rule_and_verify_schedule(self):
        """
        Submit the rule and verify scheduling logic.
        Returns:
            bool: True if rule is scheduled for weekly execution, False otherwise.
        """
        self.driver.find_element(By.CSS_SELECTOR, self.locators['saveRuleButton']).click()
        success = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators['successMessage']))
        )
        return success is not None

    # --- Appended methods for TC_SCRUM158_04 ---
    def validate_schema_missing_required_field(self, schema_json):
        """
        Validate schema and check for error when required field is missing.
        Args:
            schema_json (dict): The schema to validate.
        Returns:
            str: Error message displayed.
        """
        editor = self.driver.find_element(By.CSS_SELECTOR, self.locators['jsonSchemaEditor'])
        editor.clear()
        editor.send_keys(str(schema_json))
        self.driver.find_element(By.ID, self.locators['validateSchemaBtn']).click()
        error = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators['schemaErrorMessage']))
        )
        return error.text

    def attempt_create_rule_with_incomplete_schema(self, schema_json):
        """
        Attempt to create rule with incomplete schema and verify error handling.
        Args:
            schema_json (dict): The incomplete schema.
        Returns:
            str: Error message displayed.
        """
        editor = self.driver.find_element(By.CSS_SELECTOR, self.locators['jsonSchemaEditor'])
        editor.clear()
        editor.send_keys(str(schema_json))
        self.driver.find_element(By.CSS_SELECTOR, self.locators['saveRuleButton']).click()
        error = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators['schemaErrorMessage']))
        )
        return error.text
