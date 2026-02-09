from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    # Locators (example - update as per actual UI)
    RULES_TAB = (By.ID, "rulesTab")
    ADD_RULE_BUTTON = (By.ID, "addRuleBtn")
    RULE_NAME_INPUT = (By.ID, "ruleNameInput")
    RULE_TRIGGER_DROPDOWN = (By.ID, "ruleTriggerDropdown")
    RULE_TRIGGER_OPTION = lambda self, trigger: (By.XPATH, f"//li[text()='{trigger}']")
    JSON_RULE_INPUT = (By.ID, "jsonRuleInput")
    SAVE_RULE_BUTTON = (By.ID, "saveRuleBtn")
    SYSTEM_TIME_INPUT = (By.ID, "systemTimeInput")
    SIMULATE_TIME_BUTTON = (By.ID, "simulateTimeBtn")
    ACCEPTED_RULES_LIST = (By.ID, "acceptedRulesList")
    EXECUTED_RULES_LIST = (By.ID, "executedRulesList")
    RULE_STATUS = lambda self, rule_name: (By.XPATH, f"//tr[td[text()='{rule_name}']]/td[@class='status']")
    
    def navigate_to_rules_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.RULES_TAB)).click()
    
    def click_add_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_RULE_BUTTON)).click()
    
    def enter_rule_name(self, rule_name):
        rule_name_input = self.wait.until(EC.visibility_of_element_located(self.RULE_NAME_INPUT))
        rule_name_input.clear()
        rule_name_input.send_keys(rule_name)
    
    def select_rule_trigger(self, trigger):
        self.wait.until(EC.element_to_be_clickable(self.RULE_TRIGGER_DROPDOWN)).click()
        self.wait.until(EC.element_to_be_clickable(self.RULE_TRIGGER_OPTION(trigger))).click()
    
    def enter_json_rule(self, json_rule):
        json_input = self.wait.until(EC.visibility_of_element_located(self.JSON_RULE_INPUT))
        json_input.clear()
        json_input.send_keys(json_rule)
    
    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.SAVE_RULE_BUTTON)).click()
    
    def simulate_system_time(self, time_string):
        time_input = self.wait.until(EC.visibility_of_element_located(self.SYSTEM_TIME_INPUT))
        time_input.clear()
        time_input.send_keys(time_string)
        self.wait.until(EC.element_to_be_clickable(self.SIMULATE_TIME_BUTTON)).click()
    
    def is_rule_accepted(self, rule_name):
        accepted_rules = self.wait.until(EC.visibility_of_element_located(self.ACCEPTED_RULES_LIST)).text
        return rule_name in accepted_rules
    
    def is_rule_executed(self, rule_name):
        executed_rules = self.wait.until(EC.visibility_of_element_located(self.EXECUTED_RULES_LIST)).text
        return rule_name in executed_rules
    
    def get_rule_status(self, rule_name):
        status_elem = self.wait.until(EC.visibility_of_element_located(self.RULE_STATUS(rule_name)))
        return status_elem.text
