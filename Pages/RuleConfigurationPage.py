# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class RuleConfigurationPage(BasePage):
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

    def navigate_to_rule_creation(self):
        try:
            self.driver.get("https://app.example.com/rules/configuration")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.save_rule_button)
            )
            logging.info("Navigated to rule creation interface.")
        except TimeoutException:
            logging.error("Rule creation interface not loaded.")
            raise

    def set_trigger(self, trigger_type, date):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.trigger_type_dropdown)
            ).click()
            trigger_dropdown = self.driver.find_element(*self.trigger_type_dropdown)
            trigger_dropdown.send_keys(trigger_type)
            date_picker = self.driver.find_element(*self.date_picker)
            date_picker.clear()
            date_picker.send_keys(date)
            logging.info(f"Set trigger: {trigger_type} at {date}")
        except NoSuchElementException as e:
            logging.error("Trigger elements not found.")
            raise

    def add_condition(self, condition_type, operator, amount, currency):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.add_condition_btn)
            ).click()
            self.driver.find_element(*self.condition_type_dropdown).send_keys(condition_type)
            self.driver.find_element(*self.operator_dropdown).send_keys(operator)
            balance_input = self.driver.find_element(*self.balance_threshold_input)
            balance_input.clear()
            balance_input.send_keys(str(amount))
            logging.info(f"Added condition: {condition_type} {operator} {amount} {currency}")
        except NoSuchElementException as e:
            logging.error("Condition elements not found.")
            raise

    def add_action(self, action_type, amount, currency, destination_account):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.action_type_dropdown)
            ).click()
            self.driver.find_element(*self.action_type_dropdown).send_keys(action_type)
            self.driver.find_element(*self.transfer_amount_input).clear()
            self.driver.find_element(*self.transfer_amount_input).send_keys(str(amount))
            self.driver.find_element(*self.destination_account_input).clear()
            self.driver.find_element(*self.destination_account_input).send_keys(destination_account)
            logging.info(f"Added action: {action_type}, ${amount} to {destination_account}")
        except NoSuchElementException as e:
            logging.error("Action elements not found.")
            raise

    def save_rule(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.save_rule_button)
            ).click()
            logging.info("Rule saved.")
        except TimeoutException:
            logging.error("Save button not clickable.")
            raise

    def retrieve_rule(self, rule_id):
        try:
            self.driver.get(f"https://app.example.com/rules/{rule_id}")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.rule_id_input)
            )
            rule_details = {
                "rule_id": self.driver.find_element(*self.rule_id_input).get_attribute("value"),
                "rule_name": self.driver.find_element(*self.rule_name_input).get_attribute("value"),
            }
            logging.info(f"Retrieved rule: {rule_id}")
            return rule_details
        except TimeoutException:
            logging.error("Rule details not loaded.")
            raise

    def validate_rule_components(self, rule_id):
        try:
            self.driver.get(f"https://app.example.com/rules/{rule_id}")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.json_schema_editor)
            )
            self.driver.find_element(*self.validate_schema_btn).click()
            success = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            if success:
                logging.info("Rule validation successful.")
                return True
            else:
                error = self.driver.find_element(*self.schema_error_message).text
                logging.error(f"Rule validation failed: {error}")
                return False
        except TimeoutException:
            logging.error("Validation elements not loaded.")
            raise
