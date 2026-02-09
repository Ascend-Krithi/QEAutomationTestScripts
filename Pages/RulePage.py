import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RulePage:
    def __init__(self, driver):
        self.driver = driver

    def define_percentage_rule(self, trigger_type, percentage):
        """
        Defines a rule for percentage of deposit action.
        :param trigger_type: The type of trigger (e.g., 'after_deposit')
        :param percentage: The percentage to apply
        """
        # Locate and click 'Add Rule' button
        add_rule_btn = self.driver.find_element(By.ID, 'add-rule')
        add_rule_btn.click()
        # Select trigger type
        trigger_dropdown = self.driver.find_element(By.ID, 'trigger-type')
        trigger_dropdown.click()
        trigger_option = self.driver.find_element(By.XPATH, f"//option[@value='{trigger_type}']")
        trigger_option.click()
        # Set percentage value
        percentage_field = self.driver.find_element(By.ID, 'percentage-value')
        percentage_field.clear()
        percentage_field.send_keys(str(percentage))
        # Save rule
        save_btn = self.driver.find_element(By.ID, 'save-rule')
        save_btn.click()
        # Wait for confirmation
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.rule-success'))
        )

    def define_currency_conversion_rule(self, trigger_type, currency, amount):
        """
        Defines a rule for currency conversion (future rule type).
        :param trigger_type: The type of trigger (e.g., 'currency_conversion')
        :param currency: The currency to convert to
        :param amount: The fixed amount
        """
        add_rule_btn = self.driver.find_element(By.ID, 'add-rule')
        add_rule_btn.click()
        trigger_dropdown = self.driver.find_element(By.ID, 'trigger-type')
        trigger_dropdown.click()
        trigger_option = self.driver.find_element(By.XPATH, f"//option[@value='{trigger_type}']")
        trigger_option.click()
        currency_field = self.driver.find_element(By.ID, 'currency-field')
        currency_field.clear()
        currency_field.send_keys(currency)
        amount_field = self.driver.find_element(By.ID, 'fixed-amount')
        amount_field.clear()
        amount_field.send_keys(str(amount))
        save_btn = self.driver.find_element(By.ID, 'save-rule')
        save_btn.click()
        # Wait for either success or graceful rejection message
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located([
                (By.CSS_SELECTOR, 'div.rule-success'),
                (By.CSS_SELECTOR, 'div.rule-error')
            ])
        )

    def verify_rule_accepted(self):
        """
        Verifies that the rule was accepted.
        """
        success_msg = self.driver.find_element(By.CSS_SELECTOR, 'div.rule-success')
        return success_msg.is_displayed()

    def verify_rule_rejected_gracefully(self):
        """
        Verifies that a rule was rejected gracefully with a clear message.
        """
        error_msg = self.driver.find_element(By.CSS_SELECTOR, 'div.rule-error')
        return error_msg.is_displayed() and 'not supported' in error_msg.text.lower()

    def verify_existing_rules_execute(self):
        """
        Verifies that existing rules continue to function as expected.
        """
        rules_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.rule-item')
        for rule in rules_list:
            if 'active' in rule.get_attribute('class'):
                # Simulate execution or check status
                status = rule.find_element(By.CSS_SELECTOR, 'span.rule-status')
                if status.text.lower() != 'executed':
                    return False
        return True
