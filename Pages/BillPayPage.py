from selenium.webdriver.common.by import By
class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        self.payeeName = (By.NAME, 'payee.name')
        self.address = (By.NAME, 'payee.address.street')
        self.city = (By.NAME, 'payee.address.city')
        self.state = (By.NAME, 'payee.address.state')
        self.zipCode = (By.NAME, 'payee.address.zipCode')
        self.phoneNumber = (By.NAME, 'payee.phoneNumber')
        self.accountNumber = (By.NAME, 'payee.accountNumber')
        self.verifyAccountNumber = (By.NAME, 'verifyAccount')
        self.amount = (By.NAME, 'amount')
        self.fromAccountId = (By.NAME, 'fromAccountId')
        self.sendPaymentButton = (By.CSS_SELECTOR, "input[value='Send Payment']")
        self.successMessage = (By.ID, 'billpayResult')
        self.confPayeeName = (By.ID, 'payeeName')
        self.confAmount = (By.ID, 'amount')
        self.confFromAccount = (By.ID, 'fromAccountId')

    def enter_payee_details(self, name, address, city, state, zip, phone, account, verify_account):
        self.driver.find_element(*self.payeeName).clear()
        self.driver.find_element(*self.payeeName).send_keys(name)
        self.driver.find_element(*self.address).clear()
        self.driver.find_element(*self.address).send_keys(address)
        self.driver.find_element(*self.city).clear()
        self.driver.find_element(*self.city).send_keys(city)
        self.driver.find_element(*self.state).clear()
        self.driver.find_element(*self.state).send_keys(state)
        self.driver.find_element(*self.zipCode).clear()
        self.driver.find_element(*self.zipCode).send_keys(zip)
        self.driver.find_element(*self.phoneNumber).clear()
        self.driver.find_element(*self.phoneNumber).send_keys(phone)
        self.driver.find_element(*self.accountNumber).clear()
        self.driver.find_element(*self.accountNumber).send_keys(account)
        self.driver.find_element(*self.verifyAccountNumber).clear()
        self.driver.find_element(*self.verifyAccountNumber).send_keys(verify_account)

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount).clear()
        self.driver.find_element(*self.amount).send_keys(amount)

    def select_from_account(self, account_id):
        from selenium.webdriver.support.ui import Select
        select = Select(self.driver.find_element(*self.fromAccountId))
        select.select_by_value(account_id)

    def click_send_payment(self):
        self.driver.find_element(*self.sendPaymentButton).click()

    def get_success_message(self):
        return self.driver.find_element(*self.successMessage).text

    def get_confirmation_details(self):
        return {
            'payeeName': self.driver.find_element(*self.confPayeeName).text,
            'amount': self.driver.find_element(*self.confAmount).text,
            'fromAccount': self.driver.find_element(*self.confFromAccount).text
        }

    def is_displayed(self):
        return self.driver.find_element(*self.sendPaymentButton).is_displayed()
