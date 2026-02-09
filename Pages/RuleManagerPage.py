# RuleManagerPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class RuleManagerPage:
    def __init__(self, driver):
        self.driver = driver
        self.rule_json_input = (By.ID, 'rule-json-input')
        self.submit_rule_button = (By.ID, 'submit-rule-btn')
        self.acceptance_message = (By.CSS_SELECTOR, 'div.rule-acceptance-msg')
        self.error_message = (By.CSS_SELECTOR, 'div.rule-error-msg')

    def enter_rule_json(self, rule_json):
        rule_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_json_input)
        )
        rule_input.clear()
        rule_input.send_keys(rule_json)

    def submit_rule(self):
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_rule_button)
        )
        submit_btn.click()

    def verify_rule_accepted(self):
        acceptance = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.acceptance_message)
        )
        return 'accepted' in acceptance.text.lower()

    def verify_rule_rejected(self):
        error = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.error_message)
        )
        return 'rejected' in error.text.lower() or 'error' in error.text.lower()

    def get_latest_rule(self):
        """
        Fetch the latest rule entered and validate its fields.
        """
        # This assumes backend exposes latest rule on UI
        rule_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_json_input)
        )
        return json.loads(rule_input.get_attribute('value'))

    def load_batch_rules(self, batch_rules_json):
        rules = json.loads(batch_rules_json)
        for rule in rules:
            self.enter_rule_json(json.dumps(rule))
            self.submit_rule()
            assert self.verify_rule_accepted(), f"Rule not accepted: {rule}"

    def submit_rule_with_sql_injection(self, malicious_rule_json):
        self.enter_rule_json(malicious_rule_json)
        self.submit_rule()
        assert self.verify_rule_rejected(), "SQL injection rule was not rejected!"