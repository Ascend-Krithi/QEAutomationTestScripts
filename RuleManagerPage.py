# RuleManagerPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagerPage:
    def __init__(self, driver):
        self.driver = driver
        self.rule_json_input = (By.ID, 'rule-json-input')  # Placeholder locator
        self.submit_rule_button = (By.ID, 'submit-rule-btn')  # Placeholder locator
        self.acceptance_message = (By.CSS_SELECTOR, 'div.rule-acceptance-msg')  # Placeholder locator

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
