# Pages/LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.NAME, 'username')
        self.password_field = (By.NAME, 'password')
        self.login_button = (By.CSS_SELECTOR, "input[value='Log In']")

    def enter_username(self, username):
        username_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_field)
        )
        username_input.clear()
        username_input.send_keys(username)

    def enter_password(self, password):
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)
        )
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_btn.click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
