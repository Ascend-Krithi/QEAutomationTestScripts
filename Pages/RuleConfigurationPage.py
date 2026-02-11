import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators loaded from Locators.json
        self.locators = {
            'add_rule_button': (By.XPATH, "//button[@id='add-rule']"),
            'rule_name_input': (By.ID, "rule-name"),
            'rule_type_dropdown': (By.ID, "rule-type"),
            'advanced_tab': (By.XPATH, "//a[@id='advanced-tab']"),
            'save_button': (By.XPATH, "//button[@id='save-rule']"),
            'success_message': (By.XPATH, "//div[@class='success-message']"),
            # Add other locators as needed from Locators.json
        }
    def click_add_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.locators['add_rule_button'])).click()
    def enter_rule_name(self, name):
        rule_name = self.wait.until(EC.visibility_of_element_located(self.locators['rule_name_input']))
        rule_name.clear()
        rule_name.send_keys(name)
    def select_rule_type(self, rule_type):
        dropdown = self.wait.until(EC.visibility_of_element_located(self.locators['rule_type_dropdown']))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//option[text()='{rule_type}']")))
        option.click()
    def open_advanced_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.locators['advanced_tab'])).click()
    def configure_advanced_rule(self, settings_dict):
        # Example: settings_dict = {'priority': 'High', 'condition': 'Enabled'}
        for field, value in settings_dict.items():
            locator = (By.ID, f"advanced-{field}")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(value)
    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.locators['save_button'])).click()
    def verify_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.locators['success_message'])).is_displayed()
    def create_rule(self, rule_name, rule_type, advanced_settings=None):
        self.click_add_rule()
        self.enter_rule_name(rule_name)
        self.select_rule_type(rule_type)
        if advanced_settings:
            self.open_advanced_tab()
            self.configure_advanced_rule(advanced_settings)
        self.save_rule()
        return self.verify_success_message()
