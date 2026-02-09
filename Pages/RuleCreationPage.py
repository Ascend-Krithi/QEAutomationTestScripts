# RuleCreationPage.py
"""
Selenium Page Object for Rule Creation Workflow
Generated to cover acceptance criteria for financial automation (SCENARIO-3, SCENARIO-4).
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleCreationPage:
    """
    Page Object representing the Rule Creation Page for automated financial workflows.
    """
    URL = "https://example-finance.com/rules"

    # Locators (synthesized based on best practices)
    TRIGGER_TYPE_SELECT = (By.ID, "rule-trigger-type")
    ACTION_TYPE_SELECT = (By.ID, "rule-action-type")
    ACTION_AMOUNT_INPUT = (By.ID, "rule-action-amount")
    CONDITION_BALANCE_OPERATOR = (By.ID, "rule-condition-balance-operator")
    CONDITION_BALANCE_VALUE = (By.ID, "rule-condition-balance-value")
    CONDITION_SOURCE_SELECT = (By.ID, "rule-condition-source")
    SUBMIT_BUTTON = (By.ID, "rule-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.rule-error")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.rule-success")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to(self):
        """Navigates to the Rule Creation Page URL."""
        self.driver.get(self.URL)

    def select_trigger_type(self, trigger_type: str):
        """Selects the trigger type (e.g., 'after_deposit')."""
        trigger_select = self.wait.until(EC.element_to_be_clickable(self.TRIGGER_TYPE_SELECT))
        trigger_select.click()
        trigger_select.send_keys(trigger_type)

    def select_action_type(self, action_type: str):
        """Selects the action type (e.g., 'fixed_amount')."""
        action_select = self.wait.until(EC.element_to_be_clickable(self.ACTION_TYPE_SELECT))
        action_select.click()
        action_select.send_keys(action_type)

    def enter_action_amount(self, amount: float):
        """Enters the action amount."""
        amount_input = self.wait.until(EC.visibility_of_element_located(self.ACTION_AMOUNT_INPUT))
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_balance_condition(self, operator: str, value: float):
        """Sets balance condition (operator and value)."""
        operator_select = self.wait.until(EC.element_to_be_clickable(self.CONDITION_BALANCE_OPERATOR))
        operator_select.click()
        operator_select.send_keys(operator)
        value_input = self.wait.until(EC.visibility_of_element_located(self.CONDITION_BALANCE_VALUE))
        value_input.clear()
        value_input.send_keys(str(value))

    def set_source_condition(self, source: str):
        """Sets transaction source condition (e.g., 'salary')."""
        source_select = self.wait.until(EC.element_to_be_clickable(self.CONDITION_SOURCE_SELECT))
        source_select.click()
        source_select.send_keys(source)

    def submit_rule(self):
        """Submits the rule."""
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_error_message(self) -> str:
        """Returns the error message text if present."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except Exception:
            return ""

    def get_success_message(self) -> str:
        """Returns the success message text if present."""
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return success.text
        except Exception:
            return ""

    def validate_rule_submission(self, expected_success: bool) -> bool:
        """Validates rule submission outcome."""
        if expected_success:
            return self.get_success_message() != ""
        else:
            return self.get_error_message() != ""

"""
Documentation:
- This PageClass is strictly generated to handle rule creation for financial automation.
- Locators are synthesized to match best practices and Selenium standards.
- Methods parameterized for dynamic test data and mapped to acceptance criteria.
- Actions, validations, and error handling are included for robust downstream integration.
- Designed for maintainability and extensibility in enterprise test automation.
- Comprehensive error handling for missing/unsupported fields (SCENARIO-4).
"""
