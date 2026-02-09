"""
Page Object for Rule Configuration Page.
Implements methods for defining rules (specific_date/recurring), saving, simulating triggers, and validating rule acceptance/execution.
Locators are based on Locators.json provided.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from typing import Dict, Any
import json

class RuleConfigurationPage:
    """
    Page Object representing the Rule Configuration Page.
    Implements methods for rule creation, saving, simulation, and validation.
    """
    # Locators
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")
    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def __init__(self, driver: WebDriver):
        """
        Initialize with Selenium WebDriver.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def define_json_rule(self, rule_data: Dict[str, Any]) -> None:
        """
        Define a JSON rule in the schema editor.
        Args:
            rule_data: Rule definition as Python dict.
        """
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.click()
        # Clear and input JSON
        self.driver.execute_script("arguments[0].innerText = arguments[1];", editor, json.dumps(rule_data, indent=2))

    def select_trigger_type(self, trigger_type: str, date: str = None, interval: str = None) -> None:
        """
        Select trigger type and configure parameters.
        Args:
            trigger_type: 'specific_date' or 'recurring'
            date: ISO date string for specific_date
            interval: Interval string for recurring
        """
        dropdown = self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='trigger-type-select']/option[@value='{trigger_type}']")))
        option.click()
        if trigger_type == "specific_date" and date:
            date_input = self.wait.until(EC.element_to_be_clickable(self.date_picker))
            date_input.clear()
            date_input.send_keys(date[:10])  # YYYY-MM-DD
        elif trigger_type == "recurring" and interval:
            interval_input = self.wait.until(EC.element_to_be_clickable(self.recurring_interval_input))
            interval_input.clear()
            interval_input.send_keys(interval)

    def save_rule(self) -> None:
        """
        Click the Save Rule button to persist the rule.
        """
        save_btn = self.wait.until(EC.element_to_be_clickable(self.save_rule_button))
        save_btn.click()

    def validate_rule_acceptance(self) -> bool:
        """
        Validate that the rule is accepted by checking for success message.
        Returns:
            True if rule is accepted, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    def simulate_trigger_action(self, scenario: str) -> bool:
        """
        Simulate trigger actions (e.g., system time, recurring interval).
        Args:
            scenario: Scenario name ('SCENARIO-1' or 'SCENARIO-2').
        Returns:
            True if action executed as expected, False otherwise.
        """
        # NOTE: Actual time simulation may require backend or test hooks.
        # Here, we validate UI feedback for action execution.
        try:
            if scenario == 'SCENARIO-1':
                # Wait for transfer action success at specific date
                self.wait.until(EC.visibility_of_element_located(self.success_message))
                return True
            elif scenario == 'SCENARIO-2':
                # Wait for recurring action success
                self.wait.until(EC.visibility_of_element_located(self.success_message))
                return True
            else:
                return False
        except TimeoutException:
            return False

    def validate_rule_execution(self) -> bool:
        """
        Validate that the rule action was executed (success message).
        Returns:
            True if executed, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    def get_schema_error(self) -> str:
        """
        Retrieve schema validation error message if present.
        Returns:
            Error message string, or empty if none.
        """
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return error_elem.text
        except TimeoutException:
            return ""
