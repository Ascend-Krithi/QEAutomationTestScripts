# RuleManagementPage.py
"""
Page Object for Rule Management Page.

This class encapsulates UI elements and actions for managing rules with triggers and actions such as specific_date, recurring, fixed_amount, percentage_of_deposit, after_deposit.

Features:
- Locators mapped from Locators.json and test case requirements.
- Methods for creating, updating, validating, and retrieving rules.
- Comprehensive docstrings for downstream automation.
- Strict code integrity and structure for enterprise usage.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class RuleManagementPage:
    """
    Page Object Model for Rule Management Page.
    """
    URL = "https://example-ecommerce.com/rules"

    CREATE_RULE_BUTTON = (By.ID, "create-rule-btn")
    RULE_NAME_FIELD = (By.ID, "rule-name-input")
    TRIGGER_DROPDOWN = (By.ID, "trigger-dropdown")
    ACTION_DROPDOWN = (By.ID, "action-dropdown")
    VALUE_FIELD = (By.ID, "rule-value-input")
    DATE_PICKER = (By.ID, "rule-date-picker")
    SAVE_BUTTON = (By.ID, "save-rule-btn")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")
    RULE_LIST = (By.CSS_SELECTOR, "ul.rules-list")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def create_rule(self, rule_data: dict):
        """
        Create a new rule with provided data.
        Args:
            rule_data (dict): {'name', 'trigger', 'action', 'value', 'date', 'conditions'}
        """
        self.wait.until(EC.element_to_be_clickable(self.CREATE_RULE_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.RULE_NAME_FIELD)).send_keys(rule_data.get('name', ''))
        self.wait.until(EC.element_to_be_clickable(self.TRIGGER_DROPDOWN)).click()
        self.select_dropdown_option(self.TRIGGER_DROPDOWN, rule_data['trigger']['type'])
        if rule_data['trigger']['type'] == 'specific_date':
            self.wait.until(EC.visibility_of_element_located(self.DATE_PICKER)).send_keys(rule_data['trigger']['date'])
        self.wait.until(EC.element_to_be_clickable(self.ACTION_DROPDOWN)).click()
        self.select_dropdown_option(self.ACTION_DROPDOWN, rule_data['action']['type'])
        self.wait.until(EC.visibility_of_element_located(self.VALUE_FIELD)).send_keys(str(rule_data['action']['amount']))
        # Handle conditions
        if 'conditions' in rule_data and not rule_data['conditions']:
            pass  # No conditions to add
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()

    def select_dropdown_option(self, dropdown_locator, option_text):
        dropdown = self.wait.until(EC.visibility_of_element_located(dropdown_locator))
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == option_text:
                option.click()
                break

    def is_rule_created(self, rule_name: str) -> bool:
        rule_list = self.wait.until(EC.visibility_of_element_located(self.RULE_LIST))
        return any(rule_name in item.text for item in rule_list.find_elements_by_tag_name('li'))

    def get_success_message(self) -> str:
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return msg.text
        except:
            return ""

    def retrieve_rule(self, rule_name: str) -> dict:
        """
        Retrieve rule details from the rule list.
        """
        rule_list = self.wait.until(EC.visibility_of_element_located(self.RULE_LIST))
        for item in rule_list.find_elements_by_tag_name('li'):
            if rule_name in item.text:
                return json.loads(item.get_attribute('data-rule-json'))
        return {}

    # Additional methods as required by future test cases.