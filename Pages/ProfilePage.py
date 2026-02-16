# Executive Summary:
# This Page Object encapsulates all profile operations and is updated for the Bill Pay test cases.
from selenium.webdriver.common.by import By

class ProfilePage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_settings(self):
        settings_button = self.driver.find_element(By.XPATH, "//button[@id='settings']")
        settings_button.click()

    def update_profile(self, name, email):
        name_field = self.driver.find_element(By.XPATH, "//input[@id='name']")
        email_field = self.driver.find_element(By.XPATH, "//input[@id='email']")
        save_button = self.driver.find_element(By.XPATH, "//button[@id='saveProfile']")
        name_field.clear()
        name_field.send_keys(name)
        email_field.clear()
        email_field.send_keys(email)
        save_button.click()

    def is_profile_updated(self):
        success_msg = self.driver.find_element(By.XPATH, "//div[@id='profileSuccess']")
        return success_msg.is_displayed()
