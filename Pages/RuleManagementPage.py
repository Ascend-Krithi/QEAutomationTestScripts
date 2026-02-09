from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RuleManagementPage:
    # Placeholder locators; update as per actual UI
    DEFINE_RULE_BUTTON = (By.ID, "define-rule-btn")
    RULE_TYPE_DROPDOWN = (By.ID, "rule-type-dropdown")
    RULE_TRIGGER_DROPDOWN = (By.ID, "rule-trigger-dropdown")
    DEPOSIT_AMOUNT_INPUT = (By.ID, "deposit-amount-input")
    PERCENTAGE_INPUT = (By.ID, "percentage-input")
    FIXED_AMOUNT_INPUT = (By.ID, "fixed-amount-input")
    CURRENCY_DROPDOWN = (By.ID, "currency-dropdown")
    ACCEPT_RULE_BUTTON = (By.ID, "accept-rule-btn")
    RULE_ACCEPTED_MESSAGE = (By.CSS_SELECTOR, "div.rule-accepted")
    RULE_REJECTED_MESSAGE = (By.CSS_SELECTOR, "div.rule-rejected")
    EXECUTE_DEPOSIT_BUTTON = (By.ID, "execute-deposit-btn")
    TRANSFER_EXECUTED_MESSAGE = (By.CSS_SELECTOR, "div.transfer-executed")
    EXISTING_RULES_LIST = (By.ID, "existing-rules-list")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def define_rule(self, rule_type: str, trigger_type: str, **kwargs):
        self.driver.find_element(*self.DEFINE_RULE_BUTTON).click()
        self.driver.find_element(*self.RULE_TYPE_DROPDOWN).send_keys(rule_type)
        self.driver.find_element(*self.RULE_TRIGGER_DROPDOWN).send_keys(trigger_type)
        if 'percentage' in kwargs:
            self.driver.find_element(*self.PERCENTAGE_INPUT).clear()
            self.driver.find_element(*self.PERCENTAGE_INPUT).send_keys(str(kwargs['percentage']))
        if 'amount' in kwargs:
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).clear()
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).send_keys(str(kwargs['amount']))
        if 'currency' in kwargs:
            self.driver.find_element(*self.CURRENCY_DROPDOWN).send_keys(kwargs['currency'])
        self.driver.find_element(*self.ACCEPT_RULE_BUTTON).click()

    def get_rule_acceptance_message(self):
        try:
            return self.driver.find_element(*self.RULE_ACCEPTED_MESSAGE).text
        except Exception:
            return self.driver.find_element(*self.RULE_REJECTED_MESSAGE).text

    def simulate_deposit(self, amount: int):
        self.driver.find_element(*self.DEPOSIT_AMOUNT_INPUT).clear()
        self.driver.find_element(*self.DEPOSIT_AMOUNT_INPUT).send_keys(str(amount))
        self.driver.find_element(*self.EXECUTE_DEPOSIT_BUTTON).click()

    def get_transfer_executed_message(self):
        return self.driver.find_element(*self.TRANSFER_EXECUTED_MESSAGE).text

    def verify_existing_rules(self):
        return self.driver.find_element(*self.EXISTING_RULES_LIST).text
