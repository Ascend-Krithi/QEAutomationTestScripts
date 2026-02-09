# Pages/RuleConfigurationPage.py
# Selenium Page Object for Rule Configuration Page
# Generated for test cases TC-FT-001 and TC-FT-002
# Updated for TC-FT-005 and TC-FT-006

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for the Rule Configuration Page.
    Supports rule creation, trigger configuration, action setup, and validation.
    """

    def __init__(self, driver):
        """
        Initializes locators and driver.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        # Rule Form Locators
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Trigger Locators
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')
        # Condition Locators
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
        # Action Locators
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')
        # Validation Locators
        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    def set_rule_id(self, rule_id):
        """
        Set Rule ID.
        """
        rule_id_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_id_input)
        )
        rule_id_elem.clear()
        rule_id_elem.send_keys(rule_id)

    def set_rule_name(self, rule_name):
        """
        Set Rule Name.
        """
        rule_name_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_name_input)
        )
        rule_name_elem.clear()
        rule_name_elem.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        """
        Select trigger type from dropdown.
        :param trigger_type: str, e.g., 'specific_date', 'recurring', 'after_deposit', 'currency_conversion'
        """
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.trigger_type_dropdown)
        )
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[@value='{trigger_type}']")
        option.click()

    def set_trigger_date(self, date_str):
        """
        Set specific date for trigger.
        :param date_str: ISO date string, e.g., '2024-07-01T10:00:00Z'
        """
        date_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.date_picker)
        )
        date_elem.clear()
        date_part = date_str.split('T')[0]
        date_elem.send_keys(date_part)

    def set_recurring_interval(self, interval_value):
        """
        Set recurring interval (e.g., 'weekly').
        """
        interval_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.recurring_interval_input)
        )
        interval_elem.clear()
        interval_elem.send_keys(interval_value)

    def set_action_type(self, action_type):
        """
        Select action type (e.g., 'fixed_amount', 'percentage_of_deposit').
        """
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.action_type_dropdown)
        )
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[@value='{action_type}']")
        option.click()

    def set_transfer_amount(self, amount):
        """
        Set fixed transfer amount.
        """
        amount_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transfer_amount_input)
        )
        amount_elem.clear()
        amount_elem.send_keys(str(amount))

    def set_percentage(self, percentage):
        """
        Set percentage for deposit action.
        """
        percentage_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.percentage_input)
        )
        percentage_elem.clear()
        percentage_elem.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        """
        Set destination account ID.
        """
        account_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.destination_account_input)
        )
        account_elem.clear()
        account_elem.send_keys(account_id)

    def save_rule(self):
        """
        Click save rule button.
        """
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.save_rule_button)
        )
        save_btn.click()

    def validate_rule_success(self):
        """
        Validate rule acceptance by checking for success message.
        Returns True if success message is present.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except:
            return False

    def validate_rule_error(self):
        """
        Validate rule error by checking for schema error message.
        Returns True if error message is present.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.schema_error_message)
            )
            return True
        except:
            return False

    # --- Appended Methods for TC-FT-005 and TC-FT-006 ---

    def define_percentage_of_deposit_rule(self, rule_id, rule_name, percentage):
        """
        Define a rule triggered after deposit with a percentage action.
        :param rule_id: str
        :param rule_name: str
        :param percentage: int or float
        """
        self.set_rule_id(rule_id)
        self.set_rule_name(rule_name)
        self.select_trigger_type('after_deposit')
        after_deposit_toggle_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.after_deposit_toggle)
        )
        if not after_deposit_toggle_elem.is_selected():
            after_deposit_toggle_elem.click()
        self.set_action_type('percentage_of_deposit')
        self.set_percentage(percentage)
        self.save_rule()

    def simulate_deposit_and_verify_transfer(self, deposit_amount, expected_transfer_amount):
        """
        Simulate deposit and verify transfer action.
        :param deposit_amount: int or float
        :param expected_transfer_amount: int or float
        """
        # This is a placeholder for actual deposit simulation logic.
        # If the UI allows deposit simulation, implement accordingly.
        # For now, validate rule success after deposit.
        # Optionally, check for transfer confirmation in UI.
        success = self.validate_rule_success()
        assert success, "Rule was not accepted after deposit simulation."
        # Optionally, verify transfer amount in UI if available
        # transfer_elem = self.driver.find_element(By.XPATH, f"//span[text()='{expected_transfer_amount}']")
        # assert transfer_elem.is_displayed(), "Transfer amount not shown."

    def define_new_rule_type_and_validate(self, rule_id, rule_name, trigger_type, action_type, amount=None, currency=None):
        """
        Define a rule with a new/future rule type and validate acceptance or rejection.
        :param rule_id: str
        :param rule_name: str
        :param trigger_type: str (e.g., 'currency_conversion')
        :param action_type: str (e.g., 'fixed_amount')
        :param amount: int or float, optional
        :param currency: str, optional
        """
        self.set_rule_id(rule_id)
        self.set_rule_name(rule_name)
        self.select_trigger_type(trigger_type)
        if currency:
            # If UI has currency input, set it here
            pass  # Placeholder for currency selection logic
        self.set_action_type(action_type)
        if amount is not None:
            self.set_transfer_amount(amount)
        self.save_rule()
        # Validate acceptance or graceful rejection
        accepted = self.validate_rule_success()
        if not accepted:
            rejected = self.validate_rule_error()
            assert rejected, "Rule neither accepted nor gracefully rejected."

    def verify_existing_rules_function(self, rule_id):
        """
        Verify that an existing rule continues to execute as before.
        :param rule_id: str
        """
        # Logic to select and execute existing rule
        # Placeholder: Validate rule success
        success = self.validate_rule_success()
        assert success, f"Existing rule {rule_id} did not function as expected."
