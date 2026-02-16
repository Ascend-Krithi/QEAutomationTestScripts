# Executive Summary:
# This Page Object encapsulates settings and bill pay operations required for TC-BP-001 and TC-BP-002.
from selenium.webdriver.common.by import By

class SettingsPage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_bill_pay(self):
        bill_pay_tab = self.driver.find_element(By.XPATH, "//a[@id='billPayTab']")
        bill_pay_tab.click()

    def set_payment_account(self, account_number):
        account_field = self.driver.find_element(By.XPATH, "//input[@id='accountNumber']")
        account_field.clear()
        account_field.send_keys(account_number)

    def set_payment_amount(self, amount):
        amount_field = self.driver.find_element(By.XPATH, "//input[@id='paymentAmount']")
        amount_field.clear()
        amount_field.send_keys(str(amount))

    def submit_payment(self):
        submit_button = self.driver.find_element(By.XPATH, "//button[@id='submitPayment']")
        submit_button.click()

    def get_payment_confirmation(self):
        confirmation = self.driver.find_element(By.XPATH, "//div[@id='paymentConfirmation']")
        return confirmation.text

    def is_payment_successful(self):
        success_msg = self.driver.find_element(By.XPATH, "//div[@id='paymentSuccess']")
        return success_msg.is_displayed()
