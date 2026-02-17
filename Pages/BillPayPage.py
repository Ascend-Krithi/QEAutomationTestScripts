from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        # Form fields
        self.payee_name = (By.NAME, 'payee.name')
        self.address = (By.NAME, 'payee.address.street')
        self.city = (By.NAME, 'payee.address.city')
        self.state = (By.NAME, 'payee.address.state')
        self.zip_code = (By.NAME, 'payee.address.zipCode')
        self.phone_number = (By.NAME, 'payee.phoneNumber')
        self.account_number = (By.NAME, 'payee.accountNumber')
        self.verify_account_number = (By.NAME, 'verifyAccount')
        self.amount = (By.NAME, 'amount')
        self.from_account_id = (By.NAME, 'fromAccountId')
        self.send_payment_button = (By.CSS_SELECTOR, "input[value='Send Payment']")
        # Confirmation
        self.success_message = (By.ID, 'billpayResult')
        self.conf_payee_name = (By.ID, 'payeeName')
        self.conf_amount = (By.ID, 'amount')
        self.conf_from_account = (By.ID, 'fromAccountId')
        # Error (for mismatched accounts)
        self.error_message = (By.XPATH, "//*[contains(text(), 'Account numbers do not match')]")

    def fill_payee_info(self, name, address, city, state, zip_code, phone):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.payee_name)).clear()
        self.driver.find_element(*self.payee_name).send_keys(name)
        self.driver.find_element(*self.address).clear()
        self.driver.find_element(*self.address).send_keys(address)
        self.driver.find_element(*self.city).clear()
        self.driver.find_element(*self.city).send_keys(city)
        self.driver.find_element(*self.state).clear()
        self.driver.find_element(*self.state).send_keys(state)
        self.driver.find_element(*self.zip_code).clear()
        self.driver.find_element(*self.zip_code).send_keys(zip_code)
        self.driver.find_element(*self.phone_number).clear()
        self.driver.find_element(*self.phone_number).send_keys(phone)

    def enter_account_numbers(self, account, verify_account):
        self.driver.find_element(*self.account_number).clear()
        self.driver.find_element(*self.account_number).send_keys(account)
        self.driver.find_element(*self.verify_account_number).clear()
        self.driver.find_element(*self.verify_account_number).send_keys(verify_account)

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount).clear()
        self.driver.find_element(*self.amount).send_keys(str(amount))

    def select_from_account(self, account_id):
        select_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.from_account_id)
        )
        from selenium.webdriver.support.ui import Select
        Select(select_elem).select_by_value(str(account_id))

    def click_send_payment(self):
        send_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.send_payment_button)
        )
        send_btn.click()

    def is_success_message_displayed(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.success_message)
            ).is_displayed()
        except Exception:
            return False

    def get_confirmation_details(self):
        payee = self.driver.find_element(*self.conf_payee_name).text
        amount = self.driver.find_element(*self.conf_amount).text
        from_account = self.driver.find_element(*self.conf_from_account).text
        return {'payee': payee, 'amount': amount, 'from_account': from_account}

    def is_account_mismatch_error_displayed(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            ).is_displayed()
        except Exception:
            return False
