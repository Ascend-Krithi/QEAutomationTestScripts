# Pages/RuleConfigurationPage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    PageClass for Rule Configuration Page.
    Handles rule creation, schema validation, and simulation based on test cases TC_SCRUM158_01 and TC_SCRUM158_02.
    Uses locators from Locators.json.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Example locators loaded from Locators.json
        self.locators = {
            "create_rule_button": (By.XPATH, "//button[@id='createRule']"),
            "rule_name_input": (By.XPATH, "//input[@id='ruleName']"),
            "schema_tab": (By.XPATH, "//a[@id='schemaTab']"),
            "schema_validation_button": (By.XPATH, "//button[@id='validateSchema']"),
            "simulate_button": (By.XPATH, "//button[@id='simulateRule']"),
            "simulation_result": (By.XPATH, "//div[@id='simulationResult']"),
            # Add other locators as needed from Locators.json
        }

    def click_create_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.locators["create_rule_button"])).click()

    def enter_rule_name(self, rule_name):
        rule_name_input = self.wait.until(EC.visibility_of_element_located(self.locators["rule_name_input"]))
        rule_name_input.clear()
        rule_name_input.send_keys(rule_name)

    def open_schema_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.locators["schema_tab"])).click()

    def validate_schema(self):
        self.wait.until(EC.element_to_be_clickable(self.locators["schema_validation_button"])).click()

    def simulate_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.locators["simulate_button"])).click()

    def get_simulation_result(self):
        result_elem = self.wait.until(EC.visibility_of_element_located(self.locators["simulation_result"]))
        return result_elem.text

    # Add more methods as required by the test cases and Locators.json