# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for the Rule Configuration Page.
    Provides methods to create rules, configure triggers, actions, and validate rule schemas.
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

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
    balance_threshold_input = (By.NAME, "balance-limit")
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

    # ... existing methods ...

    def create_rule_with_minimal_schema_TC_SCRUM158_07(self):
        """
        Test Case TC_SCRUM158_07:
        1. Prepare a schema with only required fields (one trigger, one condition, one action).
        2. Submit the schema and verify rule creation, ensuring the rule is accepted and created successfully.
        """

        import json

        minimal_schema = {
            "trigger": {"type": "manual"},
            "conditions": [
                {"type": "amount", "operator": "==", "value": 1}
            ],
            "actions": [
                {"type": "transfer", "account": "G", "amount": 1}
            ]
        }

        # Wait for the JSON schema editor to be visible
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))

        # Focus and clear the editor (if possible)
        editor.click()
        editor.clear()
        # Enter JSON into the editor (if Monaco editor, send keys)
        editor.send_keys(json.dumps(minimal_schema, indent=2))

        # Click validate schema button
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn))
        validate_btn.click()

        # Wait for success message
        success = self.wait.until(EC.visibility_of_element_located(self.success_message))
        assert "success" in success.text.lower(), "Rule schema validation did not succeed"

        # Click Save Rule button to submit
        save_btn = self.wait.until(EC.element_to_be_clickable(self.save_rule_button))
        save_btn.click()

        # Confirm rule creation by checking for success message again
        rule_created = self.wait.until(EC.visibility_of_element_located(self.success_message))
        assert "created" in rule_created.text.lower(), "Rule was not created successfully"

        return True
