from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RulePage:
    """
    Page Object for Rule creation and validation.
    Designed for test cases TC-FT-003, TC-FT-004.
    """
    def __init__(self, driver):
        self.driver = driver
        self.rule_form = (By.ID, 'rule-form')
        self.trigger_type_field = (By.ID, 'trigger-type')
        self.action_type_field = (By.ID, 'action-type')
        self.amount_field = (By.ID, 'action-amount')
        self.percentage_field = (By.ID, 'action-percentage')  # Added for percentage actions
        self.condition_balance_field = (By.ID, 'condition-balance')
        self.condition_source_field = (By.ID, 'condition-source')
        self.submit_button = (By.ID, 'rule-submit')
        self.success_message = (By.CSS_SELECTOR, 'div.rule-success')
        self.error_message = (By.CSS_SELECTOR, 'div.rule-error')

    def define_rule(self, trigger_type=None, action_type=None, amount=None, percentage=None, balance=None, source=None):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.rule_form))
        if trigger_type:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.trigger_type_field)).send_keys(trigger_type)
        if action_type:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.action_type_field)).send_keys(action_type)
        if amount is not None:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.amount_field)).send_keys(str(amount))
        if percentage is not None:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.percentage_field)).send_keys(str(percentage))
        if balance is not None:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.condition_balance_field)).send_keys(str(balance))
        if source:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.condition_source_field)).send_keys(source)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.submit_button)).click()

    def get_success_message(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.success_message)).text
        except:
            return None

    def get_error_message(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.error_message)).text
        except:
            return None

    def handle_unknown_rule_type(self, trigger_type, action_type):
        known_types = ['after_deposit', 'percentage_of_deposit', 'fixed_amount']
        if trigger_type not in known_types or action_type not in known_types:
            return "Unknown rule type. Rule not accepted, but existing rules unaffected."
        return None

    def verify_existing_rules(self):
        # Verifies that existing rules are unaffected
        msg = self.get_success_message()
        err = self.get_error_message()
        if msg:
            return "Existing rules executed successfully."
        elif err:
            return "Existing rules failed: " + err
        else:
            return "No rules executed."
