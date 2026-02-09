import pytest
import asyncio

from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    # Existing test methods...
    # ... [full file content as previously pasted] ...

    @pytest.mark.asyncio
    async def test_login_without_remember_me_session_not_persisted(self):
        """
        TC_LOGIN_007: Login without 'Remember Me', verify session not persisted after browser restart
        Steps:
            1. Navigate to login
            2. Enter valid credentials without 'Remember Me'
            3. Login
            4. Close and reopen browser
            5. Verify session does not persist
        """
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.login(username="valid_user", password="valid_pass", remember_me=False)
        await login_page.close_browser()
        await login_page.reopen_browser()
        assert await login_page.verify_session_not_persisted(), "Session should not persist after browser restart when 'Remember Me' is not checked."

    @pytest.mark.asyncio
    async def test_forgot_password_flow_confirmation(self):
        """
        TC_LOGIN_008: Forgot password flow, verify confirmation
        Steps:
            1. Navigate to login
            2. Click 'Forgot Password'
            3. Enter registered email
            4. Submit
            5. Verify confirmation message
        """
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.forgot_password(email="registered_user@example.com")
        assert await login_page.verify_password_reset_confirmation(), "Password reset confirmation message not found."

class TestRuleConfiguration:
    # Existing test methods...
    # ... [full file content as previously pasted] ...
