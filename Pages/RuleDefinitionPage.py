# RuleDefinitionPage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleDefinitionPage:
    def __init__(self, driver):
        self.driver = driver
        self.rule_form = (By.ID, 'rule-form')
        self.trigger_type_field = (By.ID, 'trigger-type')
        self.action_type_field = (By.ID, 'action-type')
        self.amount_field = (By.ID, 'amount')
        self.percentage_field = (By.ID, 'percentage')  # Added for percentage actions
        self.conditions_field = (By.ID, 'conditions')
        self.submit_button = (By.ID, 'submit-rule')
        self.error_message = (By.CSS_SELECTOR, 'div.error-message')
        self.accepted_message = (By.CSS_SELECTOR, 'div.success-message')

    def navigate_to_rule_definition(self):
        self.driver.get("https://example-ecommerce.com/rule-definition")

    def define_rule(self, trigger, action, conditions):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.rule_form))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.trigger_type_field)).send_keys(trigger.get('type', ''))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.action_type_field)).send_keys(action.get('type', ''))
        if action.get('type') == 'percentage_of_deposit':
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.percentage_field)).send_keys(str(action.get('percentage', '')))
        elif action.get('type') == 'fixed_amount':
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.amount_field)).send_keys(str(action.get('amount', '')))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.conditions_field)).send_keys(str(conditions))

    def submit_rule(self):
        self.driver.find_element(*self.submit_button).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text

    def is_rule_accepted(self):
        return self.driver.find_element(*self.accepted_message).is_displayed()

    def handle_unknown_rule_type(self, trigger, action):
        # Handles future/unknown rule types gracefully
        known_types = ['after_deposit', 'percentage_of_deposit', 'fixed_amount']
        if trigger.get('type') not in known_types or action.get('type') not in known_types:
            return "Unknown rule type. Rule not accepted, but existing rules unaffected."
        return None
