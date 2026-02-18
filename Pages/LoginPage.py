from selenium.webdriver.common.by import By
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.usernameField = (By.NAME, 'username')
        self.passwordField = (By.NAME, 'password')
        self.loginButton = (By.CSS_SELECTOR, "input[value='Log In']")

    def enter_username(self, username):
        self.driver.find_element(*self.usernameField).clear()
        self.driver.find_element(*self.usernameField).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.passwordField).clear()
        self.driver.find_element(*self.passwordField).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.loginButton).click()

    def is_displayed(self):
        return self.driver.find_element(*self.loginButton).is_displayed()
