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
        await self.login_page.fill_email('')

    async def test_TC_Login_03_missing_email(self):
        login_url = "http://your-login-url.com"
        valid_password = "ValidPassword123"
        expected_error = "Email required"
        result = self.login_page.validate_login_missing_email(login_url, valid_password, expected_error)
        assert result, f"Expected error message '{expected_error}' not shown for missing email."

    async def test_TC_Login_04_missing_password(self):
        login_url = "http://your-login-url.com"
        valid_email = "user@example.com"
        expected_error = "Password required"
        result = self.login_page.validate_login_missing_password(login_url, valid_email, expected_error)
        assert result, f"Expected error message '{expected_error}' not shown for missing password."

    async def test_TC_Login_01_valid_login(self):
        login_url = "http://your-login-url.com"
        valid_email = "user@example.com"
        valid_password = "ValidPassword123"
        result = self.login_page.validate_successful_login(login_url, valid_email, valid_password)
        assert result, "Login was not successful with valid credentials."

    async def test_TC_Login_02_invalid_login(self):
        login_url = "http://your-login-url.com"
        invalid_email = "wronguser@example.com"
        invalid_password = "WrongPassword"
        expected_error = "Invalid credentials"
        result = self.login_page.validate_invalid_login(login_url, invalid_email, invalid_password, expected_error)
        assert result, f"Expected error message '{expected_error}' not shown for invalid credentials."

    async def test_TC_Login_08_forgot_password_flow(self):
        login_url = "http://your-login-url.com"
        result = self.login_page.validate_forgot_password_flow(login_url)
        assert result, "User was not redirected to password recovery page after clicking 'Forgot Password'."

    async def test_TC_Login_09_maximum_input_length_login(self):
        login_url = "http://your-login-url.com"
        max_length_email = "a" * 247 + "@ex.com"
        valid_password = "ValidPassword123"
        result = self.login_page.validate_maximum_input_length_login(login_url, max_length_email, valid_password)
        assert result, "Login was not successful or field did not accept maximum input length."

    async def test_TC_LOGIN_005_special_characters_login(self):
        login_url = "http://your-login-url.com"
        special_email = "special_user!@#$/example.com"
        special_password = "P@$$w0rd!#"
        result = self.login_page.validate_special_characters_login(login_url, special_email, special_password)
        assert result, "Special characters were not accepted or login failed."

    async def test_TC_LOGIN_006_remember_me_session_persistence(self):
        login_url = "http://your-login-url.com"
        valid_email = "user@example.com"
        valid_password = "ValidPassword123"
        result = self.login_page.validate_remember_me_login(login_url, valid_email, valid_password)
        assert result, "Remember Me checkbox was not checked or session did not persist."

    async def test_TC_LOGIN_007_remember_me_unchecked_and_session_not_persisted(self):
        login_url = "http://your-login-url.com"
        email = "user@example.com"
        password = "ValidPassword123"
        assert self.login_page.validate_remember_me_unchecked(login_url, email, password), "'Remember Me' checkbox was checked or login failed."
        assert self.login_page.validate_session_not_persisted(login_url, email, password), "Session persisted after browser restart, expected logout."

    async def test_TC_LOGIN_008_forgot_password_flow(self):
        login_url = "http://your-login-url.com"
        email = "user@example.com"
        result = self.login_page.validate_forgot_password_flow(login_url)
        assert result, "Password reset flow failed or confirmation message not displayed."

    # --- TC_LOGIN_009 ---
    async def test_TC_LOGIN_009_rapid_invalid_login_attempts(self):
        """
        TC_LOGIN_009: Attempt to login with invalid credentials rapidly multiple times (10x).
        Validates if system applies rate limiting, lockout, or captcha.
        """
        login_url = "http://your-login-url.com"
        email = "wronguser@example.com"
        password = "WrongPassword"
        attempts = 10
        detected = self.login_page.validate_rapid_invalid_login_attempts(login_url, email, password, attempts)
        assert detected["rate_limit"] or detected["lockout"] or detected["captcha"], "System did not detect rate limiting, lockout, or captcha after rapid invalid login attempts."
        if detected["errors"]:
            print("Detection details:", detected["errors"])

    # --- TC_LOGIN_010 ---
    async def test_TC_LOGIN_010_case_sensitivity_in_login(self):
        """
        TC_LOGIN_010: Enter email/username and password with different cases (upper/lower/mixed).
        Validates that login succeeds only if credentials match exactly; error otherwise.
        """
        login_url = "http://your-login-url.com"
        email_variants = [
            "USER@EXAMPLE.COM",
            "user@example.com",
            "User@Example.Com",
            "UsEr@ExAmPlE.cOm"
        ]
        password = "ValidPassword123"
        results = self.login_page.validate_case_sensitivity_in_login(login_url, email_variants, password)
        for variant, success in results.items():
            if variant == "user@example.com":
                assert success, f"Login failed for correct case variant: {variant}"
            else:
                assert not success, f"Login succeeded for incorrect case variant: {variant}"
            print(f"Variant: {variant}, Success: {success}")
