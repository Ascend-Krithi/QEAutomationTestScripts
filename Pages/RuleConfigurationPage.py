# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
import datetime
import time

class RuleConfigurationPage:
    """
    Page Object for Rule Configuration Page.
    Implements methods for defining rules with specific_date and recurring triggers,
    simulating system time for trigger execution, and validating rule acceptance and execution.
    """

    # Locators from Locators.json
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")

    add_condition_btn = (By.ID, "add-condition-link")
    condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
    transaction_source_dropdown = (By.ID, "source-provider-select")
    operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")

    action_type_dropdown = (By.ID, "action-type-select")
    transfer_amount_input = (By.NAME, "fixed-amount")
    percentage_input = (By.ID, "deposit-percentage")
    destination_account_input = (By.ID, "target-account-id")

    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def define_rule_specific_date(self, rule_id: str, rule_name: str, trigger_date: str, amount: float):
        """
        Define a rule with trigger type 'specific_date' and fixed amount action.
        :param rule_id: Rule identifier
        :param rule_name: Rule name
        :param trigger_date: ISO date string (YYYY-MM-DD)
        :param amount: Amount to transfer
        """
        self.wait.until(EC.visibility_of_element_located(self.rule_id_input)).send_keys(rule_id)
        self.wait.until(EC.visibility_of_element_located(self.rule_name_input)).send_keys(rule_name)
        # Set trigger type
        Select(self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))).select_by_visible_text("specific_date")
        # Set date
        date_elem = self.wait.until(EC.visibility_of_element_located(self.date_picker))
        date_elem.clear()
        date_elem.send_keys(trigger_date)
        # Set action type
        Select(self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown))).select_by_visible_text("fixed_amount")
        # Set amount
        self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input)).clear()
        self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input)).send_keys(str(amount))
        # Save rule
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def define_rule_recurring_weekly(self, rule_id: str, rule_name: str, percentage: float):
        """
        Define a rule with trigger type 'recurring', interval 'weekly', and percentage action.
        :param rule_id: Rule identifier
        :param rule_name: Rule name
        :param percentage: Percentage of deposit to transfer
        """
        self.wait.until(EC.visibility_of_element_located(self.rule_id_input)).send_keys(rule_id)
        self.wait.until(EC.visibility_of_element_located(self.rule_name_input)).send_keys(rule_name)
        # Set trigger type
        Select(self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))).select_by_visible_text("recurring")
        # Set interval
        interval_elem = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
        interval_elem.clear()
        interval_elem.send_keys("weekly")
        # Set action type
        Select(self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown))).select_by_visible_text("percentage_of_deposit")
        # Set percentage
        self.wait.until(EC.visibility_of_element_located(self.percentage_input)).clear()
        self.wait.until(EC.visibility_of_element_located(self.percentage_input)).send_keys(str(percentage))
        # Save rule
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def simulate_system_time(self, target_datetime: datetime.datetime):
        """
        Simulate system time reaching the trigger date.
        This is a placeholder. Actual implementation would require system-level time mocking or backend API.
        """
        # Wait until system time matches target_datetime (for demo only, not production safe)
        now = datetime.datetime.utcnow()
        wait_seconds = (target_datetime - now).total_seconds()
        if wait_seconds > 0:
            time.sleep(wait_seconds)

    def simulate_weekly_intervals(self, weeks: int, interval_callback):
        """
        Simulate passing of several weeks and execute callback at each interval.
        :param weeks: Number of weeks to simulate
        :param interval_callback: Function to call at each interval
        """
        for week in range(weeks):
            interval_callback(week)
            # Simulate waiting for a week (for demo, reduce to seconds)
            time.sleep(1)  # Replace with actual time simulation if possible

    def validate_rule_acceptance(self):
        """
        Validate that rule is accepted by the system.
        Returns True if success message is found, False otherwise.
        """
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return success is not None
        except TimeoutException:
            return False

    def validate_rule_execution(self):
        """
        Validate that transfer action is executed.
        Returns True if success message is found after execution, False otherwise.
        """
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return success is not None
        except TimeoutException:
            return False

    def validate_schema(self):
        """
        Click validate schema button and check for success or error message.
        Returns 'success' or 'error' depending on outcome.
        """
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return 'success'
        except TimeoutException:
            try:
                self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
                return 'error'
            except TimeoutException:
                return 'unknown'
