# Pages/BillPayPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
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
        # Confirmation locators
        self.success_message = (By.ID, 'billpayResult')
        self.conf_payee_name = (By.ID, 'payeeName')
        self.conf_amount = (By.ID, 'amount')
        self.conf_from_account = (By.ID, 'fromAccountId')

    def fill_payee_info(self, name, address, city, state, zip_code, phone, acc_num, verify_acc_num):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.payee_name)).clear()
        self.driver.find_element(*self.payee_name).send_keys(name)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.address)).clear()
        self.driver.find_element(*self.address).send_keys(address)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.city)).clear()
        self.driver.find_element(*self.city).send_keys(city)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.state)).clear()
        self.driver.find_element(*self.state).send_keys(state)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.zip_code)).clear()
        self.driver.find_element(*self.zip_code).send_keys(zip_code)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.phone_number)).clear()
        self.driver.find_element(*self.phone_number).send_keys(phone)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.account_number)).clear()
        self.driver.find_element(*self.account_number).send_keys(acc_num)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.verify_account_number)).clear()
        self.driver.find_element(*self.verify_account_number).send_keys(verify_acc_num)

    def select_from_account(self, account_id):
        from_account_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.from_account_id)
        )
        from_account_dropdown.send_keys(account_id)

    def enter_amount(self, amount):
        amount_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.amount)
        )
        amount_field.clear()
        amount_field.send_keys(str(amount))

    def click_send_payment(self):
        send_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.send_payment_button)
        )
        send_btn.click()

    def get_confirmation_details(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.success_message))
        payee = self.driver.find_element(*self.conf_payee_name).text
        amount = self.driver.find_element(*self.conf_amount).text
        from_account = self.driver.find_element(*self.conf_from_account).text
        return {
            "payee": payee,
            "amount": amount,
            "from_account": from_account
        }
