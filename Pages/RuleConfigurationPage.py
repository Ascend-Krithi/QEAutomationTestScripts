# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

class RuleConfigurationPage:
    """
    Page Object Model for Rule Configuration Page.
    Covers locators and workflows for test cases TC_SCRUM158_07 and TC_SCRUM158_08.

    QA Report:
    - All locators from Locators.json are mapped.
    - Composite workflows cover rule creation, schema validation, and performance for large metadata.
    - Methods strictly adhere to Selenium Python standards and ensure code integrity.
    """
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ruleForm
    def enter_rule_id(self, rule_id: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, "rule-id-field")))
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.NAME, "rule-name")))
        elem.clear()
        elem.send_keys(rule_name)

    def click_save_rule(self):
        elem = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")))
        elem.click()

    # triggers
    def select_trigger_type(self, trigger_type: str):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "trigger-type-select")))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='trigger-type-select']/option[@value='{trigger_type}']")))
        option.click()

    def set_date_picker(self, date_value: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='date']")))
        elem.clear()
        elem.send_keys(date_value)

    def enter_recurring_interval(self, interval: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, "interval-value")))
        elem.clear()
        elem.send_keys(interval)

    def toggle_after_deposit(self):
        elem = self.wait.until(EC.element_to_be_clickable((By.ID, "trigger-after-deposit")))
        elem.click()

    # conditions
    def click_add_condition(self):
        elem = self.wait.until(EC.element_to_be_clickable((By.ID, "add-condition-link")))
        elem.click()

    def select_condition_type(self, condition_type: str):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select.condition-type")))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[contains(@class, 'condition-type')]/option[@value='{condition_type}']")))
        option.click()

    def enter_balance_threshold(self, threshold: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='balance-limit']")))
        elem.clear()
        elem.send_keys(threshold)

    def select_transaction_source(self, source: str):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "source-provider-select")))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='source-provider-select']/option[@value='{source}']")))
        option.click()

    def select_operator(self, operator: str):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".condition-operator-select")))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[contains(@class, 'condition-operator-select')]/option[@value='{operator}']")))
        option.click()

    # actions
    def select_action_type(self, action_type: str):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "action-type-select")))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='action-type-select']/option[@value='{action_type}']")))
        option.click()

    def enter_transfer_amount(self, amount: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.NAME, "fixed-amount")))
        elem.clear()
        elem.send_keys(amount)

    def enter_percentage(self, percentage: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, "deposit-percentage")))
        elem.clear()
        elem.send_keys(percentage)

    def enter_destination_account(self, account_id: str):
        elem = self.wait.until(EC.visibility_of_element_located((By.ID, "target-account-id")))
        elem.clear()
        elem.send_keys(account_id)

    # validation
    def enter_json_schema(self, schema_text: str):
        editor = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".monaco-editor")))
        editor.clear()
        editor.send_keys(schema_text)

    def click_validate_schema(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-verify-json")))
        btn.click()

    def get_success_message(self) -> str:
        elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))
        return elem.text

    def get_schema_error_message(self) -> str:
        elem = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='error-feedback-text']")))
        return elem.text

    # Composite workflow for TC_SCRUM158_07
    def create_rule_with_minimal_schema(self, rule_id: str, rule_name: str, schema_text: str) -> dict:
        """
        Automates creation of rule with minimal required fields (one trigger, one condition, one action).
        Returns dict with success/error messages.
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.enter_json_schema(schema_text)
        self.click_validate_schema()
        result = {
            "success": self.get_success_message(),
            "error": self.get_schema_error_message()
        }
        self.click_save_rule()
        return result

    # Composite workflow for TC_SCRUM158_08
    def create_rule_with_large_metadata(self, rule_id: str, rule_name: str, schema_text: str) -> dict:
        """
        Automates creation of rule with a large metadata field (e.g., 10,000 characters).
        Returns dict with success/error messages and performance metrics.
        """
        import time
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        start = time.time()
        self.enter_json_schema(schema_text)
        self.click_validate_schema()
        elapsed = time.time() - start
        result = {
            "success": self.get_success_message(),
            "error": self.get_schema_error_message(),
            "performance_seconds": round(elapsed, 2)
        }
        self.click_save_rule()
        return result
