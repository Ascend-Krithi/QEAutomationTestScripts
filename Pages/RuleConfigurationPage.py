# Pages/RuleConfigurationPage.py
# Selenium Page Object for Rule Configuration Page
# Generated for test cases TC-FT-001 and TC-FT-002
# Updated for TC-FT-005 and TC-FT-006

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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
        self.wait = WebDriverWait(driver, 20)
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
        rule_id_elem = self.wait.until(
            EC.visibility_of_element_located(self.rule_id_input)
        )
        rule_id_elem.clear()
        rule_id_elem.send_keys(rule_id)

    def set_rule_name(self, rule_name):
        rule_name_elem = self.wait.until(
            EC.visibility_of_element_located(self.rule_name_input)
        )
        rule_name_elem.clear()
        rule_name_elem.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.trigger_type_dropdown)
        )
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[@value='{trigger_type}']")
        option.click()

    def set_trigger_date(self, date_str):
        date_elem = self.wait.until(
            EC.visibility_of_element_located(self.date_picker)
        )
        date_elem.clear()
        date_part = date_str.split('T')[0]
        date_elem.send_keys(date_part)

    def set_recurring_interval(self, interval_value):
        interval_elem = self.wait.until(
            EC.visibility_of_element_located(self.recurring_interval_input)
        )
        interval_elem.clear()
        interval_elem.send_keys(interval_value)

    def set_action_type(self, action_type):
        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.action_type_dropdown)
        )
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[@value='{action_type}']")
        option.click()

    def set_transfer_amount(self, amount):
        amount_elem = self.wait.until(
            EC.visibility_of_element_located(self.transfer_amount_input)
        )
        amount_elem.clear()
        amount_elem.send_keys(str(amount))

    def set_percentage(self, percentage):
        percentage_elem = self.wait.until(
            EC.visibility_of_element_located(self.percentage_input)
        )
        percentage_elem.clear()
        percentage_elem.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        account_elem = self.wait.until(
            EC.visibility_of_element_located(self.destination_account_input)
        )
        account_elem.clear()
        account_elem.send_keys(account_id)

    def save_rule(self):
        save_btn = self.wait.until(
            EC.element_to_be_clickable(self.save_rule_button)
        )
        save_btn.click()

    def validate_rule_success(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except Exception:
            return False

    def validate_rule_error(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.schema_error_message)
            )
            return True
        except Exception:
            return False

    # --- Appended Methods for TC_SCRUM158_07 and TC_SCRUM158_08 ---
    def enter_json_schema(self, schema_str):
        """
        Enters the provided JSON schema into the Monaco editor.
        """
        editor = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".monaco-editor"))
        )
        try:
            textarea = editor.find_element(By.CSS_SELECTOR, "textarea")
            textarea.click()
            textarea.send_keys(Keys.CONTROL + "a")
            textarea.send_keys(Keys.DELETE)
            textarea.send_keys(schema_str)
        except Exception:
            editor.click()
            editor.send_keys(Keys.CONTROL + "a")
            editor.send_keys(Keys.DELETE)
            editor.send_keys(schema_str)

    def validate_schema(self):
        """
        Clicks the Validate Schema button to validate the entered JSON schema.
        """
        validate_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-verify-json"))
        )
        validate_btn.click()

    def get_success_message(self):
        """
        Returns the success message text if present after schema validation.
        """
        try:
            success = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
            )
            return success.text
        except Exception:
            return None

    def get_error_message(self):
        """
        Returns the error message text if present after schema validation.
        """
        try:
            error = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
            if error.is_displayed():
                return error.text
            else:
                return None
        except Exception:
            return None
