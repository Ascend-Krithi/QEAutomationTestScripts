# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for the Login Page.
    Handles actions and validations for login functionality.
    """
    # Locators (Assumed, update with actual values from Locators.json when available)
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    ERROR_MESSAGE = (By.ID, 'loginError')

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def enter_username(self, username: str):
        username_field = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str):
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def get_error_message(self) -> str:
        error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error_elem.text
