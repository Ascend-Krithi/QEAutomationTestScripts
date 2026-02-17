from selenium.webdriver.common.by import By

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        self.payee_name_input = (By.ID, 'payee-name')
        self.account_input = (By.ID, 'account')
        self.amount_input = (By.ID, 'amount')
        self.send_payment_button = (By.ID, 'send-payment-btn')
        self.success_message = (By.ID, 'success-msg')

    def enter_payee_name(self, payee_name):
        self.driver.find_element(*self.payee_name_input).clear()
        self.driver.find_element(*self.payee_name_input).send_keys(payee_name)

    def enter_account(self, account):
        self.driver.find_element(*self.account_input).clear()
        self.driver.find_element(*self.account_input).send_keys(account)

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount_input).clear()
        self.driver.find_element(*self.amount_input).send_keys(amount)

    def click_send_payment(self):
        self.driver.find_element(*self.send_payment_button).click()

    def is_payment_successful(self):
        return self.driver.find_element(*self.success_message).is_displayed()
