import pytest
import asyncio

from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    # Existing test methods...
    # ... [existing methods here] ...

    @pytest.mark.asyncio
    async def test_login_without_remember_me_session_not_persisted(self):
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.login(username="valid_user", password="valid_pass", remember_me=False)
        await login_page.close_browser()
        await login_page.reopen_browser()
        assert await login_page.verify_session_not_persisted(), "Session should not persist after browser restart when 'Remember Me' is not checked."

    @pytest.mark.asyncio
    async def test_forgot_password_flow_confirmation(self):
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.forgot_password(email="registered_user@example.com")
        assert await login_page.verify_password_reset_confirmation(), "Password reset confirmation message not found."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_001_valid_login_dashboard_redirection(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        login_page.login("user@example.com", "ValidPass123")
        # Add assertion for dashboard redirection

    @pytest.mark.asyncio
    async def test_TC_LOGIN_002_invalid_login_error_message(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        login_page.login("user@example.com", "WrongPass456")
        assert login_page.verify_invalid_credentials_error(), "Error message 'Invalid credentials' was not displayed."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_003_email_required_error(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        error_message = login_page.login_with_empty_email("ValidPass123")
        assert error_message == "Email/Username required", "Error message 'Email/Username required' was not displayed."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_004_password_required_error(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        error_message = login_page.login_with_empty_password("user@example.com")
        assert error_message == "Password required", "Error message 'Password required' was not displayed."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_007_forgot_password_flow(self):
        """
        Implements TC_LOGIN_007:
        1. Navigate to the login page.
        2. Click the 'Forgot Password' link.
        3. Verify presence of password recovery form.
        """
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page("https://example.com/login")
        login_page.click_forgot_password()
        assert login_page.verify_password_recovery_form(), "Password recovery form is not displayed."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_008_sql_injection_login(self):
        """
        Implements TC_LOGIN_008:
        1. Navigate to the login page.
        2. Enter SQL injection string in email and password fields.
        3. Click login button and verify error message 'Invalid credentials'.
        """
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page("https://example.com/login")
        sql_email = "' OR 1=1;--"
        sql_password = "' OR 1=1;--"
        login_page.sql_injection_login_test(sql_email, sql_password)
        # Error assertion is inside sql_injection_login_test
