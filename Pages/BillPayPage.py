# BillPayPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Form fields
        self.payeeName = (By.NAME, "payee.name")
        self.address = (By.NAME, "payee.address.street")
        self.city = (By.NAME, "payee.address.city")
        self.state = (By.NAME, "payee.address.state")
        self.zipCode = (By.NAME, "payee.zipCode")
        self.phoneNumber = (By.NAME, "payee.phoneNumber")
        self.accountNumber = (By.NAME, "payee.accountNumber")
        self.verifyAccountNumber = (By.NAME, "verifyAccount")
        self.amount = (By.NAME, "amount")
        self.fromAccountId = (By.NAME, "fromAccountId")
        self.sendPaymentButton = (By.CSS_SELECTOR, "input[value='Send Payment']")
        # Confirmation fields
        self.successMessage = (By.ID, "billpayResult")
        self.confPayeeName = (By.ID, "payeeName")
        self.confAmount = (By.ID, "amount")
        self.confFromAccount = (By.ID, "fromAccountId")

    def enter_payee_details(self, name, address, city, state, zip_code, phone, account, verify_account):
        self.wait.until(EC.visibility_of_element_located(self.payeeName)).send_keys(name)
        self.driver.find_element(*self.address).send_keys(address)
        self.driver.find_element(*self.city).send_keys(city)
        self.driver.find_element(*self.state).send_keys(state)
        self.driver.find_element(*self.zipCode).send_keys(zip_code)
        self.driver.find_element(*self.phoneNumber).send_keys(phone)
        self.driver.find_element(*self.accountNumber).send_keys(account)
        self.driver.find_element(*self.verifyAccountNumber).send_keys(verify_account)

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount).clear()
        self.driver.find_element(*self.amount).send_keys(str(amount))

    def select_account(self, account_id):
        self.driver.find_element(*self.fromAccountId).send_keys(str(account_id))

    def click_send_payment(self):
        self.driver.find_element(*self.sendPaymentButton).click()

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.successMessage)).text

    def get_confirmation_details(self):
        return {
            "payee_name": self.driver.find_element(*self.confPayeeName).text,
            "amount": self.driver.find_element(*self.confAmount).text,
            "from_account": self.driver.find_element(*self.confFromAccount).text
        }

    def is_error_displayed(self):
        # Generic error check, can be expanded based on app
        try:
            error = self.driver.find_element(By.CLASS_NAME, "error")
            return error.is_displayed(), error.text
        except:
            return False, ""

    def is_session_expired(self):
        # Check for session expiration message
        try:
            msg = self.driver.find_element(By.XPATH, "//*[contains(text(),'Session expired please login again')]")
            return msg.is_displayed()
        except:
            return False
