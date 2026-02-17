from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, 'username')
        self.password_input = (By.NAME, 'password')
        self.login_button = (By.CSS_SELECTOR, "input[value='Log In']")

    def enter_username(self, username):
        username_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        )
        username_elem.clear()
        username_elem.send_keys(username)

    def enter_password(self, password):
        password_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input)
        )
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_btn.click()
