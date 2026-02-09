# RuleConfigurationPage.py
"""
Executive Summary:
This PageClass enables end-to-end Selenium automation for rule creation and schema validation in the Rule Configuration module. It supports scenarios including minimal schema creation, large metadata handling, and validation feedback, strictly adhering to locator mapping and best practices.

Detailed Analysis:
- Implements locators from provided Locators.json.
- Handles form filling, schema submission, and validation feedback.
- Supports test cases TC_SCRUM158_07 and TC_SCRUM158_08.

Implementation Guide:
- Use with Selenium WebDriver (Python).
- Methods: create_rule_from_schema, validate_json_schema, handle_large_metadata, verify_rule_creation, get_validation_feedback.

Quality Assurance Report:
- Code integrity ensured via strict locator mapping.
- No existing logic overwritten; new file created.
- Includes error handling, validation checks, and clear method separation.

Troubleshooting Guide:
- If locators change, update LOCATORS dict.
- Ensure WebDriver is initialized and points to correct page.
- Check for element visibility before interaction.

Future Considerations:
- Extend for additional triggers, conditions, actions.
- Integrate with downstream automation pipelines.

"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

LOCATORS = {
    "ruleForm": {
        "ruleIdInput": (By.ID, "rule-id-field"),
        "ruleNameInput": (By.NAME, "rule-name"),
        "saveRuleButton": (By.CSS_SELECTOR, "button[data-testid='save-rule-btn'")
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
        "balanceThresholdInput": (By.CSS_SELECTOR, "input[name='balance-limit'"),
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

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def create_rule_from_schema(self, schema):
        """
        Fills the rule form based on the schema dict.
        Supports minimal schema (TC_SCRUM158_07) and large metadata (TC_SCRUM158_08).
        """
        # Example: {'trigger': {'type': 'manual'}, 'conditions': [{'type': 'amount', 'operator': '==', 'value': 1}], 'actions': [{'type': 'transfer', 'account': 'G', 'amount': 1}]}
        # Fill trigger type
        trigger_type = schema.get('trigger', {}).get('type', None)
        if trigger_type:
            dropdown = self.wait.until(EC.visibility_of_element_located(LOCATORS['triggers']['triggerTypeDropdown']))
            dropdown.send_keys(trigger_type)

        # Add conditions
        conditions = schema.get('conditions', [])
        for cond in conditions:
            add_btn = self.wait.until(EC.element_to_be_clickable(LOCATORS['conditions']['addConditionBtn']))
            add_btn.click()
            cond_type = cond.get('type', None)
            if cond_type:
                cond_type_dropdown = self.wait.until(EC.visibility_of_element_located(LOCATORS['conditions']['conditionTypeDropdown']))
                cond_type_dropdown.send_keys(cond_type)
            operator = cond.get('operator', None)
            if operator:
                operator_dropdown = self.wait.until(EC.visibility_of_element_located(LOCATORS['conditions']['operatorDropdown']))
                operator_dropdown.send_keys(operator)
            value = cond.get('value', None)
            if value is not None:
                balance_input = self.wait.until(EC.visibility_of_element_located(LOCATORS['conditions']['balanceThresholdInput']))
                balance_input.clear()
                balance_input.send_keys(str(value))
            source = cond.get('source', None)
            if source:
                src_dropdown = self.wait.until(EC.visibility_of_element_located(LOCATORS['conditions']['transactionSourceDropdown']))
                src_dropdown.send_keys(source)

        # Add actions
        actions = schema.get('actions', [])
        for action in actions:
            action_type = action.get('type', None)
            if action_type:
                action_dropdown = self.wait.until(EC.visibility_of_element_located(LOCATORS['actions']['actionTypeDropdown']))
                action_dropdown.send_keys(action_type)
            amount = action.get('amount', None)
            if amount is not None:
                amt_input = self.wait.until(EC.visibility_of_element_located(LOCATORS['actions']['transferAmountInput']))
                amt_input.clear()
                amt_input.send_keys(str(amount))
            percentage = action.get('percentage', None)
            if percentage is not None:
                pct_input = self.wait.until(EC.visibility_of_element_located(LOCATORS['actions']['percentageInput']))
                pct_input.clear()
                pct_input.send_keys(str(percentage))
            account = action.get('account', None)
            if account:
                dest_input = self.wait.until(EC.visibility_of_element_located(LOCATORS['actions']['destinationAccountInput']))
                dest_input.send_keys(account)

        # Save rule
        save_btn = self.wait.until(EC.element_to_be_clickable(LOCATORS['ruleForm']['saveRuleButton']))
        save_btn.click()

    def validate_json_schema(self, schema_json):
        """
        Inputs schema JSON into the editor and triggers validation.
        Returns validation feedback.
        """
        editor = self.wait.until(EC.visibility_of_element_located(LOCATORS['validation']['jsonSchemaEditor']))
        editor.clear()
        editor.send_keys(json.dumps(schema_json))
        validate_btn = self.wait.until(EC.element_to_be_clickable(LOCATORS['validation']['validateSchemaBtn']))
        validate_btn.click()
        try:
            success = self.wait.until(EC.visibility_of_element_located(LOCATORS['validation']['successMessage']))
            return {'status': 'success', 'message': success.text}
        except TimeoutException:
            error = self.driver.find_element(*LOCATORS['validation']['schemaErrorMessage'])
            return {'status': 'error', 'message': error.text}

    def handle_large_metadata(self, metadata):
        """
        Handles insertion of large metadata (e.g., 10,000 chars).
        """
        editor = self.wait.until(EC.visibility_of_element_located(LOCATORS['validation']['jsonSchemaEditor']))
        editor.clear()
        editor.send_keys(metadata)

    def verify_rule_creation(self):
        """
        Verifies if rule creation succeeded based on success message.
        """
        try:
            success = self.wait.until(EC.visibility_of_element_located(LOCATORS['validation']['successMessage']))
            return True
        except TimeoutException:
            return False

    def get_validation_feedback(self):
        """
        Returns the validation feedback message.
        """
        try:
            success = self.wait.until(EC.visibility_of_element_located(LOCATORS['validation']['successMessage']))
            return success.text
        except TimeoutException:
            error = self.driver.find_element(*LOCATORS['validation']['schemaErrorMessage'])
            return error.text
