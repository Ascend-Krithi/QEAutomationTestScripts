# RuleConfigurationPage.py
"""
Selenium PageClass for Rule Configuration Page

This class encapsulates all interactions for the Rule Configuration Page, based on Locators.json.

Coding Standards:
- Follows PEP8 and Selenium Python best practices.
- All locators are loaded from Locators.json.
- Methods are atomic and descriptive.
- Comprehensive docstrings provided.

Author: Enterprise Test Automation Orchestration Agent
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    PageClass for Rule Configuration Page.
    """
    def __init__(self, driver: WebDriver, locators: dict):
        """
        :param driver: Selenium WebDriver instance
        :param locators: Dict of locators from Locators.json
        """
        self.driver = driver
        self.locators = locators["RuleConfigurationPage"]
        self.wait = WebDriverWait(driver, 10)

    # --- Rule Form ---
    def set_rule_id(self, rule_id: str):
        """Set Rule ID field."""
        rule_id_input = self.driver.find_element(By.ID, "rule-id-field")
        rule_id_input.clear()
        rule_id_input.send_keys(rule_id)

    def set_rule_name(self, rule_name: str):
        """Set Rule Name field."""
        rule_name_input = self.driver.find_element(By.NAME, "rule-name")
        rule_name_input.clear()
        rule_name_input.send_keys(rule_name)

    def click_save_rule(self):
        """Click Save Rule button."""
        save_btn = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        save_btn.click()

    # --- Triggers ---
    def select_trigger_type(self, trigger_type: str):
        """Select trigger type from dropdown."""
        dropdown = self.driver.find_element(By.ID, "trigger-type-select")
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='trigger-type-select']/option[text()='{trigger_type}']")
        option.click()

    def set_trigger_date(self, date_value: str):
        """Set trigger date."""
        date_picker = self.driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        date_picker.clear()
        date_picker.send_keys(date_value)

    def set_recurring_interval(self, interval: str):
        """Set recurring interval."""
        interval_input = self.driver.find_element(By.ID, "interval-value")
        interval_input.clear()
        interval_input.send_keys(interval)

    def toggle_after_deposit(self):
        """Toggle 'After Deposit' switch."""
        toggle = self.driver.find_element(By.ID, "trigger-after-deposit")
        toggle.click()

    # --- Conditions ---
    def click_add_condition(self):
        """Click Add Condition button."""
        add_btn = self.driver.find_element(By.ID, "add-condition-link")
        add_btn.click()

    def select_condition_type(self, condition_type: str):
        """Select condition type from dropdown."""
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "select.condition-type")
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[contains(@class, 'condition-type')]/option[text()='{condition_type}']")
        option.click()

    def set_balance_threshold(self, threshold: str):
        """Set balance threshold value."""
        threshold_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")
        threshold_input.clear()
        threshold_input.send_keys(threshold)

    def select_transaction_source(self, source: str):
        """Select transaction source from dropdown."""
        dropdown = self.driver.find_element(By.ID, "source-provider-select")
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='source-provider-select']/option[text()='{source}']")
        option.click()

    def select_operator(self, operator: str):
        """Select operator from dropdown."""
        dropdown = self.driver.find_element(By.CSS_SELECTOR, ".condition-operator-select")
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[contains(@class, 'condition-operator-select')]/option[text()='{operator}']")
        option.click()

    # --- Actions ---
    def select_action_type(self, action_type: str):
        """Select action type from dropdown."""
        dropdown = self.driver.find_element(By.ID, "action-type-select")
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='action-type-select']/option[text()='{action_type}']")
        option.click()

    def set_transfer_amount(self, amount: str):
        """Set transfer amount."""
        amount_input = self.driver.find_element(By.NAME, "fixed-amount")
        amount_input.clear()
        amount_input.send_keys(amount)

    def set_percentage(self, percentage: str):
        """Set deposit percentage."""
        percentage_input = self.driver.find_element(By.ID, "deposit-percentage")
        percentage_input.clear()
        percentage_input.send_keys(percentage)

    def set_destination_account(self, account_id: str):
        """Set destination account ID."""
        account_input = self.driver.find_element(By.ID, "target-account-id")
        account_input.clear()
        account_input.send_keys(account_id)

    # --- Validation ---
    def edit_json_schema(self, schema_text: str):
        """Edit JSON schema in Monaco editor."""
        editor = self.driver.find_element(By.CSS_SELECTOR, ".monaco-editor")
        editor.click()
        editor.clear()
        editor.send_keys(schema_text)

    def click_validate_schema(self):
        """Click Validate Schema button."""
        validate_btn = self.driver.find_element(By.ID, "btn-verify-json")
        validate_btn.click()

    def get_success_message(self):
        """Get success message after validation."""
        try:
            msg = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))
            return msg.text
        except Exception:
            return None

    def get_schema_error_message(self):
        """Get schema error message after validation."""
        try:
            msg = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='error-feedback-text']")))
            return msg.text
        except Exception:
            return None
