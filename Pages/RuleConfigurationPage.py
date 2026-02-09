# imports
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RuleConfigurationPage:
    """
    Page Object Model for Rule Configuration Page.
    """

    # Locators loaded from Locators.json context
    _locators = {
        "ruleForm": {
            "ruleIdInput": (By.ID, "rule-id-field"),
            "ruleNameInput": (By.NAME, "rule-name"),
            "saveRuleButton": (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        },
        "triggers": {
            "triggerTypeDropdown": (By.ID, "trigger-type-select"),
            "datePicker": (By.CSS_SELECTOR, "input[type='date']"),
            "recurringIntervalInput": (By.ID, "interval-value"),
            "afterDepositToggle": (By.ID, "trigger-after-deposit")
        },
        "conditions": {
            "addConditionBtn": (By.ID, "add-condition-link"),
            "conditionTypeDropdown": (By.CSS_SELECTOR, "select.condition-type"),
            "balanceThresholdInput": (By.CSS_SELECTOR, "input[name='balance-limit']"),
            "transactionSourceDropdown": (By.ID, "source-provider-select"),
            "operatorDropdown": (By.CSS_SELECTOR, ".condition-operator-select")
        },
        "actions": {
            "actionTypeDropdown": (By.ID, "action-type-select"),
            "transferAmountInput": (By.NAME, "fixed-amount"),
            "percentageInput": (By.ID, "deposit-percentage"),
            "destinationAccountInput": (By.ID, "target-account-id")
        },
        "validation": {
            "jsonSchemaEditor": (By.CSS_SELECTOR, ".monaco-editor"),
            "validateSchemaBtn": (By.ID, "btn-verify-json"),
            "successMessage": (By.CSS_SELECTOR, ".alert-success"),
            "schemaErrorMessage": (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
        }
    }

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Form Interactions ---

    def enter_rule_id(self, rule_id):
        elem = self.wait.until(EC.visibility_of_element_located(self._locators["ruleForm"]["ruleIdInput"]))
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        elem = self.wait.until(EC.visibility_of_element_located(self._locators["ruleForm"]["ruleNameInput"]))
        elem.clear()
        elem.send_keys(rule_name)

    def click_save_rule(self):
        btn = self.wait.until(EC.element_to_be_clickable(self._locators["ruleForm"]["saveRuleButton"]))
        btn.click()

    # --- Schema Editor & Validation ---

    def prepare_rule_schema(self, schema_dict):
        """
        Prepares rule schema in JSON editor.
        :param schema_dict: dict representing the rule schema, including metadata.
        """
        editor = self.wait.until(EC.visibility_of_element_located(self._locators["validation"]["jsonSchemaEditor"]))
        # Monaco editor is not a standard input; use JS to set value
        schema_json = json.dumps(schema_dict, indent=2)
        self.driver.execute_script("""
            const editor = document.querySelector(arguments[0]);
            if (editor && editor.__monaco) {
                editor.__monaco.setValue(arguments[1]);
            } else {
                // fallback: set value in textarea if present
                const textarea = editor.querySelector('textarea');
                if (textarea) textarea.value = arguments[1];
            }
        """, self._locators["validation"]["jsonSchemaEditor"][1], schema_json)

    def validate_schema(self):
        """
        Clicks validate schema button and waits for result.
        :return: (success: bool, message: str)
        """
        self.wait.until(EC.element_to_be_clickable(self._locators["validation"]["validateSchemaBtn"])).click()
        try:
            success_elem = self.wait.until(
                EC.visibility_of_element_located(self._locators["validation"]["successMessage"])
            )
            return True, success_elem.text
        except TimeoutException:
            try:
                error_elem = self.driver.find_element(*self._locators["validation"]["schemaErrorMessage"])
                return False, error_elem.text
            except NoSuchElementException:
                return False, "Unknown validation error."

    # --- Rule Submission (API Simulation) ---

    def submit_rule(self):
        """
        Clicks Save Rule button to submit the schema.
        """
        self.click_save_rule()

    # --- Rule Retrieval (UI Simulation) ---

    def retrieve_rule(self, rule_id):
        """
        Retrieves rule details by rule_id.
        (Assumes rule is displayed in UI after creation; implement as needed.)
        :param rule_id: str
        :return: dict of rule details (simulate or implement UI extraction)
        """
        # Example: After saving, rule details appear in a summary panel
        try:
            rule_id_elem = self.wait.until(EC.visibility_of_element_located(self._locators["ruleForm"]["ruleIdInput"]))
            rule_name_elem = self.wait.until(EC.visibility_of_element_located(self._locators["ruleForm"]["ruleNameInput"]))
            return {
                "rule_id": rule_id_elem.get_attribute("value"),
                "rule_name": rule_name_elem.get_attribute("value")
            }
        except TimeoutException:
            return {}

    def get_metadata_from_schema(self):
        """
        Extracts metadata from schema editor content.
        :return: dict of metadata
        """
        # Monaco editor content extraction via JS
        schema_json = self.driver.execute_script("""
            const editor = document.querySelector(arguments[0]);
            if (editor && editor.__monaco) {
                return editor.__monaco.getValue();
            } else {
                // fallback: get value from textarea if present
                const textarea = editor.querySelector('textarea');
                if (textarea) return textarea.value;
                return '';
            }
        """, self._locators["validation"]["jsonSchemaEditor"][1])
        try:
            schema_dict = json.loads(schema_json)
            return schema_dict.get("metadata", {})
        except Exception:
            return {}

    def validate_metadata(self, expected_metadata):
        """
        Validates metadata in schema editor against expected values.
        :param expected_metadata: dict
        :return: bool
        """
        actual_metadata = self.get_metadata_from_schema()
        return actual_metadata == expected_metadata

    # --- Schema Error Handling ---

    def get_schema_error_message(self):
        """
        Returns schema validation error message, if present.
        """
        try:
            error_elem = self.driver.find_element(*self._locators["validation"]["schemaErrorMessage"])
            return error_elem.text
        except NoSuchElementException:
            return None

    # --- Additional Utilities ---

    def is_schema_valid(self):
        """
        Checks if schema validation succeeded.
        :return: bool
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self._locators["validation"]["successMessage"]))
            return True
        except TimeoutException:
            return False

    def is_schema_invalid(self):
        """
        Checks if schema validation failed.
        :return: bool
        """
        try:
            self.driver.find_element(*self._locators["validation"]["schemaErrorMessage"])
            return True
        except NoSuchElementException:
            return False
