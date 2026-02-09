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

    # --- Appended methods for TC_SCRUM158_09 ---
    def create_rule_specific_date_fixed_amount(self, date_iso, amount):
        """
        Create and store a rule with a specific_date trigger and fixed_amount action.
        Args:
            date_iso (str): ISO date string, e.g., '2024-07-01T10:00:00Z'
            amount (int): Fixed amount for the action
        """
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['add_rule_button']))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['trigger_type_dropdown']))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['trigger_specific_date_option']))).click()
        date_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['trigger_date_field'])))
        date_field.clear()
        date_field.send_keys(date_iso)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['action_type_dropdown']))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['action_fixed_amount_option']))).click()
        amount_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['action_amount_field'])))
        amount_field.clear()
        amount_field.send_keys(str(amount))
        # No conditions to add
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['save_rule_button']))).click()
        # Wait for success confirmation
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['rule_success_toast'])))

    def retrieve_and_verify_rule_specific_date(self, date_iso, amount):
        """
        Retrieve the rule from backend and verify it matches the original input.
        Args:
            date_iso (str): ISO date string
            amount (int): Fixed amount
        Returns:
            bool: True if rule matches, False otherwise
        """
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['refresh_rules_button']))).click()
        rule_rows = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.locators['rule_table_rows'])))
        for row in rule_rows:
            trigger = row.find_element(By.XPATH, self.locators['rule_row_trigger']).text
            action = row.find_element(By.XPATH, self.locators['rule_row_action']).text
            if trigger == f"Specific Date: {date_iso}" and action == f"Fixed Amount: {amount}":
                return True
        return False

    # --- Appended methods for TC_SCRUM158_10 ---
    def create_rule_after_deposit_fixed_amount_unconditional(self, amount):
        """
        Create a rule with after_deposit trigger, fixed_amount action, and empty conditions (unconditional).
        Args:
            amount (int): Fixed amount for the action
        """
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['add_rule_button']))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['trigger_type_dropdown']))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['trigger_after_deposit_option']))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['action_type_dropdown']))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['action_fixed_amount_option']))).click()
        amount_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['action_amount_field'])))
        amount_field.clear()
        amount_field.send_keys(str(amount))
        # No conditions to add
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['save_rule_button']))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['rule_success_toast'])))

    def simulate_deposit_and_verify_unconditional_rule(self, deposit_amount, expected_transfer_amount):
        """
        Simulate deposit to trigger unconditional rule and verify transfer is executed.
        Args:
            deposit_amount (int): Amount to deposit
            expected_transfer_amount (int): Expected transfer amount
        Returns:
            bool: True if transfer executed, False otherwise
        """
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['deposit_button']))).click()
        deposit_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['deposit_amount_field'])))
        deposit_field.clear()
        deposit_field.send_keys(str(deposit_amount))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators['confirm_deposit_button']))).click()
        # Wait for rule execution (transfer confirmation)
        transfer_toast = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['transfer_success_toast'])))
        transfer_text = transfer_toast.text
        return str(expected_transfer_amount) in transfer_text
