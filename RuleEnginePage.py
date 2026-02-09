# RuleEnginePage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import json
import datetime

class RuleEnginePage:
    """
    PageClass for Rule Engine operations in AXOS automation suite.
    Supports rule definition, deposit simulation, currency conversion, and log verification.
    Updated for TC-FT-005 and TC-FT-006.
    """
    # Selectors for rule engine UI
    RULE_JSON_INPUT = (By.ID, "rule-json-input")
    SUBMIT_RULE_BUTTON = (By.ID, "submit-rule-btn")
    ACCEPTANCE_MESSAGE = (By.CSS_SELECTOR, "div.rule-accepted")
    EXECUTION_LOG = (By.ID, "execution-log")
    DEPOSIT_SIMULATION_INPUT = (By.ID, "deposit-sim-input")  # Assumed selector
    DEPOSIT_SIMULATE_BUTTON = (By.ID, "deposit-sim-btn")    # Assumed selector
    CURRENCY_CONVERSION_INPUT = (By.ID, "currency-conv-input") # Assumed selector
    CURRENCY_CONVERSION_BUTTON = (By.ID, "currency-conv-btn")  # Assumed selector
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.rule-error")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def define_rule(self, rule_data: dict):
        """
        Defines a rule in the Rule Engine using provided rule_data.
        """
        rule_json = json.dumps(rule_data)
        self.driver.find_element(*self.RULE_JSON_INPUT).clear()
        self.driver.find_element(*self.RULE_JSON_INPUT).send_keys(rule_json)
        self.driver.find_element(*self.SUBMIT_RULE_BUTTON).click()

    def is_rule_accepted(self):
        """
        Checks if rule is accepted based on UI feedback.
        """
        elements = self.driver.find_elements(*self.ACCEPTANCE_MESSAGE)
        return len(elements) > 0 and elements[0].is_displayed()

    def get_error_message(self):
        """
        Retrieves error message for rejected rules.
        """
        elements = self.driver.find_elements(*self.ERROR_MESSAGE)
        return elements[0].text if elements else None

    def simulate_deposit(self, amount: float):
        """
        Simulates a deposit action for rule execution.
        """
        self.driver.find_element(*self.DEPOSIT_SIMULATION_INPUT).clear()
        self.driver.find_element(*self.DEPOSIT_SIMULATION_INPUT).send_keys(str(amount))
        self.driver.find_element(*self.DEPOSIT_SIMULATE_BUTTON).click()

    def verify_transfer_action(self, expected_amount: float):
        """
        Verifies transfer action log for expected transfer amount.
        """
        log = self.get_execution_log()
        return f"Transfer of {expected_amount} units executed" in log

    def define_currency_conversion_rule(self, rule_data: dict):
        """
        Defines a currency conversion rule and handles expected system response.
        """
        rule_json = json.dumps(rule_data)
        self.driver.find_element(*self.RULE_JSON_INPUT).clear()
        self.driver.find_element(*self.RULE_JSON_INPUT).send_keys(rule_json)
        self.driver.find_element(*self.SUBMIT_RULE_BUTTON).click()

    def simulate_currency_conversion(self, currency: str):
        """
        Simulates currency conversion trigger for rule execution.
        """
        self.driver.find_element(*self.CURRENCY_CONVERSION_INPUT).clear()
        self.driver.find_element(*self.CURRENCY_CONVERSION_INPUT).send_keys(currency)
        self.driver.find_element(*self.CURRENCY_CONVERSION_BUTTON).click()

    def get_execution_log(self):
        """
        Retrieves execution log from Rule Engine.
        """
        log_element = self.driver.find_element(*self.EXECUTION_LOG)
        return log_element.text

    def verify_existing_rules_function(self):
        """
        Verifies that existing rules continue to execute as expected.
        """
        log = self.get_execution_log()
        return "Existing rule executed" in log

    # Existing methods for time/recurring triggers remain unchanged
    def simulate_time_trigger(self, trigger_date: str):
        # Placeholder for time simulation interface
        pass

    def simulate_recurring_trigger(self, interval: str, times: int):
        # Placeholder for recurring simulation interface
        pass

    def verify_transfer_action_recurring(self, expected_intervals: int):
        log = self.get_execution_log()
        return log.count("Transfer action executed at interval") == expected_intervals
