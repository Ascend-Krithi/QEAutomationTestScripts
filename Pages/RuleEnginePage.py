from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RuleEnginePage:
    """
    PageClass for rule definition and deposit simulation actions.
    Locators are placeholders and must be updated when UI details are available.
    """
    # Locators (Placeholder - update when UI details available)
    DEFINE_RULE_BUTTON = (By.ID, "define-rule-btn")
    RULE_TYPE_DROPDOWN = (By.ID, "rule-type-dropdown")
    PERCENTAGE_INPUT = (By.ID, "percentage-input")
    FIXED_AMOUNT_INPUT = (By.ID, "fixed-amount-input")
    CURRENCY_DROPDOWN = (By.ID, "currency-dropdown")
    ACCEPT_RULE_BUTTON = (By.ID, "accept-rule-btn")
    DEPOSIT_INPUT = (By.ID, "deposit-input")
    SIMULATE_DEPOSIT_BUTTON = (By.ID, "simulate-deposit-btn")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.success-message")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error-message")
    EXISTING_RULES_LIST = (By.ID, "existing-rules-list")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str):
        self.driver.get(url)

    def define_rule(self, rule_data: dict):
        """
        rule_data example:
        {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        """
        self.driver.find_element(*self.DEFINE_RULE_BUTTON).click()
        # Select rule type
        rule_type = rule_data.get("trigger", {}).get("type", "")
        self.driver.find_element(*self.RULE_TYPE_DROPDOWN).send_keys(rule_type)
        action = rule_data.get("action", {})
        if action.get("type") == "percentage_of_deposit":
            self.driver.find_element(*self.PERCENTAGE_INPUT).clear()
            self.driver.find_element(*self.PERCENTAGE_INPUT).send_keys(str(action.get("percentage", "")))
        elif action.get("type") == "fixed_amount":
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).clear()
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).send_keys(str(action.get("amount", "")))
        # Currency conversion
        if rule_type == "currency_conversion":
            self.driver.find_element(*self.CURRENCY_DROPDOWN).send_keys(rule_data.get("trigger", {}).get("currency", ""))
        # Accept rule
        self.driver.find_element(*self.ACCEPT_RULE_BUTTON).click()

    def simulate_deposit(self, amount: int):
        self.driver.find_element(*self.DEPOSIT_INPUT).clear()
        self.driver.find_element(*self.DEPOSIT_INPUT).send_keys(str(amount))
        self.driver.find_element(*self.SIMULATE_DEPOSIT_BUTTON).click()

    def get_success_message(self):
        return self.driver.find_element(*self.SUCCESS_MESSAGE).text

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def list_existing_rules(self):
        rules = self.driver.find_elements(*self.EXISTING_RULES_LIST)
        return [rule.text for rule in rules]
