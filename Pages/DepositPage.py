import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DepositPage:
    def __init__(self, driver):
        self.driver = driver

    def simulate_deposit(self, amount):
        """
        Simulates a deposit of the given amount.
        :param amount: The amount to deposit
        """
        deposit_field = self.driver.find_element(By.ID, 'deposit-amount')
        deposit_field.clear()
        deposit_field.send_keys(str(amount))
        deposit_btn = self.driver.find_element(By.ID, 'deposit-submit')
        deposit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.deposit-success'))
        )

    def verify_transfer_executed(self, expected_transfer):
        """
        Verifies that the transfer of expected units is executed.
        :param expected_transfer: The expected transfer amount
        """
        transfer_msg = self.driver.find_element(By.CSS_SELECTOR, 'div.transfer-success')
        return str(expected_transfer) in transfer_msg.text
