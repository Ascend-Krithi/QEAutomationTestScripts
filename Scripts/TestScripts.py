
class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email(''

    async def test_TC_Login_03_missing_email(self):
        """
        TC_Login_03: Navigate to login page, leave email empty, enter valid password, click login, validate 'Email required' error.
        """
        login_url = "http://your-login-url.com"  # Replace with actual login page URL
        valid_password = "ValidPassword123"      # Replace with actual valid password
        expected_error = "Email required"
        result = self.login_page.validate_login_missing_email(login_url, valid_password, expected_error)
        assert result, f"Expected error message '{expected_error}' not shown for missing email."

    async def test_TC_Login_04_missing_password(self):
        """
        TC_Login_04: Navigate to login page, enter valid email, leave password empty, click login, validate 'Password required' error.
        """
        login_url = "http://your-login-url.com"  # Replace with actual login page URL
        valid_email = "user@example.com"         # Replace with actual valid email
        expected_error = "Password required"
        result = self.login_page.validate_login_missing_password(login_url, valid_email, expected_error)
        assert result, f"Expected error message '{expected_error}' not shown for missing password."

    async def test_TC_Login_01_valid_login(self):
        """
        TC_Login_01: Navigate to login page, enter valid email and password, click login, validate login success.
        """
        login_url = "http://your-login-url.com"  # Replace with actual login page URL
        valid_email = "user@example.com"
        valid_password = "ValidPassword123"
        result = self.login_page.validate_successful_login(login_url, valid_email, valid_password)
        assert result, "Login was not successful with valid credentials."

    async def test_TC_Login_02_invalid_login(self):
        """
        TC_Login_02: Navigate to login page, enter invalid email and password, click login, validate error message 'Invalid credentials'.
        """
        login_url = "http://your-login-url.com"  # Replace with actual login page URL
        invalid_email = "wronguser@example.com"
        invalid_password = "WrongPassword"
        expected_error = "Invalid credentials"
        result = self.login_page.validate_invalid_login(login_url, invalid_email, invalid_password, expected_error)
        assert result, f"Expected error message '{expected_error}' not shown for invalid credentials."

    async def test_TC_Login_08_forgot_password_flow(self):
        """
        TC_Login_08: Navigate to login page, click 'Forgot Password', validate redirection to password recovery page.
        """
        login_url = "http://your-login-url.com"  # Replace with actual login page URL
        result = self.login_page.validate_forgot_password_flow(login_url)
        assert result, "User was not redirected to password recovery page after clicking 'Forgot Password'."

    async def test_TC_Login_09_maximum_input_length_login(self):
        """
        TC_Login_09: Navigate to login page, enter maximum allowed input for email/username (255 chars) and valid password, click login, validate acceptance and login success.
        """
        login_url = "http://your-login-url.com"  # Replace with actual login page URL
        max_length_email = "a" * 247 + "@ex.com"  # 255 chars total
        valid_password = "ValidPassword123"
        result = self.login_page.validate_maximum_input_length_login(login_url, max_length_email, valid_password)
        assert result, "Login was not successful or field did not accept maximum input length."
