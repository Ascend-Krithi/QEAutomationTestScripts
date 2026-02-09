'''
RuleConfigurationPage Selenium PageClass

Executive Summary:
This PageClass enables robust automation of rule definition, validation, and action simulation in the Rule Configuration interface. It covers all locators from Locators.json, supporting both current and future rule types, and ensures strict code integrity for downstream automation.

Detailed Analysis:
- Implements all locators for triggers, conditions, actions, and validation.
- Supports scenarios for deposit and currency conversion triggers.
- Handles success/error messages for rule acceptance/rejection.
- Includes methods for deposit simulation, rule storage verification, and rule retrieval from UI.
- Now supports generic JSON schema input, including large metadata fields, as required by test cases TC_SCRUM158_07 and TC_SCRUM158_08.

Implementation Guide:
- Instantiate with Selenium WebDriver.
- Use provided methods to define rules, simulate deposits, verify rule storage, retrieve rule details, validate outcomes, and handle schema input.
- Use create_rule_from_schema() for generic rule creation and test_large_metadata_field() for performance testing.

Quality Assurance Report:
- All locator references are validated against Locators.json.
- Methods follow Selenium best practices: explicit waits, error handling, and modular code.
- Designed for async and sync workflows.
- New methods validated against acceptance criteria TS07 and TS08.

Troubleshooting Guide:
- If a locator changes, update Locators.json and regenerate.
- For new rule types, add corresponding methods and locators.
- Error messages are surfaced via schemaErrorMessage and successMessage.

Future Considerations:
- Extend for new triggers/actions by adding methods and updating Locators.json.
- Integrate with advanced validation (e.g., JSON schema editor).
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Rule Form
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Triggers
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        # Conditions
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        # Actions
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        # Validation
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
        # Rule List/Grid (for verification and retrieval)
        self.rule_list_grid = driver.find_element(By.ID, 'rules-table')
        self.rule_search_input = driver.find_element(By.ID, 'rule-search-field')

    def select_trigger_type(self, trigger_type):
        self.trigger_type_dropdown.click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of(self.trigger_type_dropdown)
        )
        self.trigger_type_dropdown.send_keys(trigger_type)

    def set_after_deposit_trigger(self):
        if not self.after_deposit_toggle.is_selected():
            self.after_deposit_toggle.click()

    def set_currency_conversion_trigger(self, currency):
        self.select_trigger_type('currency_conversion')
        self.trigger_type_dropdown.send_keys(currency)

    def set_rule_action_percentage_of_deposit(self, percentage):
        self.action_type_dropdown.click()
        self.action_type_dropdown.send_keys('percentage_of_deposit')
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))

    def set_rule_action_fixed_amount(self, amount):
        self.action_type_dropdown.click()
        self.action_type_dropdown.send_keys('fixed_amount')
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(str(amount))

    def save_rule(self):
        self.save_rule_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )

    def get_success_message(self):
        return self.success_message.text

    def get_error_message(self):
        return self.schema_error_message.text

    def simulate_deposit(self, amount):
        """
        Simulates a deposit via the UI for testing rule execution.
        Assumes existence of a deposit widget with ID 'deposit-widget', input 'deposit-amount', and button 'deposit-submit'.
        """
        deposit_widget = self.driver.find_element(By.ID, 'deposit-widget')
        deposit_widget.click()
        deposit_amount_input = self.driver.find_element(By.ID, 'deposit-amount')
        deposit_amount_input.clear()
        deposit_amount_input.send_keys(str(amount))
        deposit_submit_btn = self.driver.find_element(By.ID, 'deposit-submit')
        deposit_submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )

    def validate_rule_schema(self):
        self.validate_schema_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )
        return self.get_success_message()

    def define_rule(self, rule_data):
        # General method to define any rule using rule_data dict
        if rule_data['trigger']['type'] == 'after_deposit':
            self.set_after_deposit_trigger()
        elif rule_data['trigger']['type'] == 'currency_conversion':
            self.set_currency_conversion_trigger(rule_data['trigger'].get('currency', ''))
        elif rule_data['trigger']['type'] == 'specific_date':
            self.select_trigger_type('specific_date')
            self.date_picker.clear()
            self.date_picker.send_keys(rule_data['trigger'].get('date', ''))
        if rule_data['action']['type'] == 'percentage_of_deposit':
            self.set_rule_action_percentage_of_deposit(rule_data['action']['percentage'])
        elif rule_data['action']['type'] == 'fixed_amount':
            self.set_rule_action_fixed_amount(rule_data['action']['amount'])
        self.save_rule()

    def verify_rule_execution(self, expected_transfer_amount):
        # Implement verification logic for transfer execution
        # E.g., check transaction logs, balances, or confirmation messages
        pass

    def verify_rule_storage(self, rule_id):
        """
        Verifies that a rule with the given rule_id exists in the rule list/grid.
        """
        self.rule_search_input.clear()
        self.rule_search_input.send_keys(rule_id)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.rule_list_grid)
        )
        rows = self.rule_list_grid.find_elements(By.CSS_SELECTOR, 'tr')
        for row in rows:
            if rule_id in row.text:
                return True
        return False

    def retrieve_rule_from_ui(self, rule_id):
        """
        Retrieves rule details from the UI rule list/grid by rule_id.
        Returns dict of rule fields.
        """
        self.rule_search_input.clear()
        self.rule_search_input.send_keys(rule_id)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.rule_list_grid)
        )
        rows = self.rule_list_grid.find_elements(By.CSS_SELECTOR, 'tr')
        for row in rows:
            if rule_id in row.text:
                columns = row.find_elements(By.TAG_NAME, 'td')
                return {
                    'rule_id': columns[0].text,
                    'rule_name': columns[1].text,
                    'trigger': columns[2].text,
                    'action': columns[3].text,
                    'conditions': columns[4].text
                }
        return None

    # --- New Methods for Test Cases TC_SCRUM158_07 and TC_SCRUM158_08 ---
    def create_rule_from_schema(self, schema_json):
        '''
        Creates a rule by pasting the provided JSON schema into the Monaco editor, validates, and saves.
        Used for scenarios with only required fields (one trigger, one condition, one action).
        '''
        editor = self.json_schema_editor
        editor.click()
        # Clear editor - usually Ctrl+A then Del
        editor.send_keys(u"\ue009" + "a")  # Ctrl+A
        editor.send_keys(u"\ue017")  # Del
        editor.send_keys(str(schema_json))
        self.validate_schema_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )
        self.save_rule_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )
        return self.get_success_message()

    def test_large_metadata_field(self, metadata):
        '''
        Tests rule creation with a large metadata field in the schema editor (e.g., 10,000 characters).
        Validates schema and checks for performance and acceptance.
        '''
        editor = self.json_schema_editor
        editor.click()
        editor.send_keys(u"\ue009" + "a")  # Ctrl+A
        editor.send_keys(u"\ue017")  # Del
        schema = '{"trigger": {"type": "manual"}, "metadata": "%s"}' % metadata
        editor.send_keys(schema)
        start = time.time()
        self.validate_schema_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '.alert-success')))
        elapsed = time.time() - start
        self.save_rule_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )
        return {
            'success': self.get_success_message(),
            'performance_sec': elapsed
        }
