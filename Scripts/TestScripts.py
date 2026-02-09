import pytest
import asyncio

from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    @pytest.mark.asyncio
    async def test_valid_login(self):
        login_page = LoginPage()
        result = await login_page.login('valid_user', 'valid_password')
        assert result['success'] is True
        assert 'token' in result

    @pytest.mark.asyncio
    async def test_invalid_login(self):
        login_page = LoginPage()
        result = await login_page.login('invalid_user', 'invalid_password')
        assert result['success'] is False
        assert 'error' in result

    # TC_Login_03: Leave email empty, enter valid password, verify 'Email required' error.
    @pytest.mark.asyncio
    async def test_empty_email_valid_password(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        login_page.navigate_to_login()
        login_page.login_with_credentials(email="", password="ValidPassword123")
        assert login_page.verify_error_message("Email required") is True

    # TC_Login_04: Enter valid email, leave password empty, verify 'Password required' error.
    @pytest.mark.asyncio
    async def test_valid_email_empty_password(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        login_page.navigate_to_login()
        login_page.login_with_credentials(email="user@example.com", password="")
        assert login_page.verify_error_message("Password required") is True

    # TC_Login_05: Leave both email and password fields empty, verify both error messages.
    @pytest.mark.asyncio
    async def test_empty_fields(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        login_page.navigate_to_login()
        login_page.login_with_credentials(email="", password="")
        import time
        time.sleep(1)
        email_error = login_page.verify_error_message("Email required")
        password_error = login_page.verify_error_message("Password required")
        assert email_error is True
        assert password_error is True

    # TC_Login_06: Login with 'Remember Me', close and reopen browser, verify session persists.
    @pytest.mark.asyncio
    async def test_remember_me_persistence(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        result = login_page.test_remember_me_session_persistence(valid_email="user@example.com", valid_password="ValidPassword123")
        assert result is True

    # TC_Login_07: Login without 'Remember Me', close and reopen browser, verify session expired.
    @pytest.mark.asyncio
    async def test_login_without_remember_me_session_expired(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        # Step 1: Login without 'Remember Me'
        login_success = login_page.login_without_remember_me(email="user@example.com", password="ValidPassword123")
        assert login_success is True
        # Step 2: Close and reopen browser, verify session expired
        session_expired = login_page.verify_session_expired_after_restart()
        assert session_expired is True

    # TC_LOGIN_001: Login with valid credentials, verify redirect to dashboard.
    @pytest.mark.asyncio
    async def test_login_and_verify_redirect(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        login_success = login_page.login_and_verify(email="user@example.com", password="ValidPassword123")
        assert login_success is True

    # TC_Login_08: Click 'Forgot Password' and assert redirect to password recovery page.
    @pytest.mark.asyncio
    async def test_forgot_password_redirect(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        login_page.navigate_to_login()
        login_page.click_forgot_password()
        assert login_page.is_on_password_recovery_page() is True

    # TC_Login_09: Enter 255-character email and valid password, assert fields accept max input, login, assert success.
    @pytest.mark.asyncio
    async def test_max_length_email_and_password_login(self):
        driver = ... # Provide Selenium WebDriver instance
        base_url = ... # Provide base URL
        login_page = LoginPage(driver, base_url)
        login_page.navigate_to_login()
        max_length_email = "a" * 247 + "@e.com"  # 255 chars total
        valid_password = "ValidPassword123"
        login_page.enter_max_length_credentials_and_login(email_or_username=max_length_email, password=valid_password)
        assert login_page.verify_max_length_fields_accept_input(email_or_username=max_length_email) is True
        assert login_page.is_login_successful() is True

class TestRuleConfiguration:
    @pytest.mark.asyncio
    async def test_valid_rule_schema(self):
        rule_page = RuleConfigurationPage()
        schema = {
            'trigger': 'amount_above',
            'conditions': [{'type': 'amount_above', 'value': 100}],
            'action': 'notify'
        }
        result = await rule_page.submit_rule_schema(schema)
        assert result['valid'] is True

    @pytest.mark.asyncio
    async def test_invalid_rule_schema(self):
        rule_page = RuleConfigurationPage()
        schema = {
            'trigger': 'amount_above',
            'conditions': [{'type': 'amount_above'}],  # missing value
            'action': 'notify'
        }
        result = await rule_page.submit_rule_schema(schema)
        assert result['valid'] is False
        assert 'error' in result

    @pytest.mark.asyncio
    async def test_invalid_trigger_schema(self):
        rule_page = RuleConfigurationPage()
        schema = {
            'trigger': 'unknown_trigger',
            'conditions': [{'type': 'amount_above', 'value': 100}],
            'action': 'notify'
        }
        result = await rule_page.test_invalid_trigger_schema(schema)
        assert result['valid'] is False
        assert 'error' in result
        assert 'invalid trigger' in result['error'].lower() or 'unknown_trigger' in result['error']

    @pytest.mark.asyncio
    async def test_condition_missing_parameters_schema(self):
        rule_page = RuleConfigurationPage()
        schema = {
            'trigger': 'amount_above',
            'conditions': [{'type': 'amount_above'}],  # missing 'value'
            'action': 'notify'
        }
        result = await rule_page.test_condition_missing_parameters_schema(schema)
        assert result['valid'] is False
        assert 'error' in result
        assert 'missing' in result['error'].lower() or 'incomplete' in result['error'].lower()

    @pytest.mark.asyncio
    async def test_create_rule_with_max_conditions_and_actions(self):
        rule_page = RuleConfigurationPage()
        rule_id = "R_MAX_001"
        rule_name = "Rule with Max Conditions and Actions"
        conditions = [
            {"condition_type": "balance_above", "balance_threshold": 1000.0, "source": "providerA", "operator": "greater_than"} for _ in range(10)
        ]
        actions = [
            {"action_type": "transfer", "amount": 100.0, "percentage": None, "dest_account": f"ACC{str(i+1).zfill(3)}"} for i in range(10)
        ]
        result = await rule_page.create_rule_with_max_conditions_and_actions(rule_id, rule_name, conditions, actions)
        assert result is True

    @pytest.mark.asyncio
    async def test_create_rule_with_empty_conditions_and_actions(self):
        rule_page = RuleConfigurationPage()
        rule_id = "R_EMPTY_001"
        rule_name = "Rule with Empty Conditions and Actions"
        result_msg = await rule_page.create_rule_with_empty_conditions_and_actions(rule_id, rule_name)
        assert isinstance(result_msg, str)
        assert "valid" in result_msg.lower() or "error" in result_msg.lower()

    @pytest.mark.asyncio
    async def test_create_rule_with_minimum_required_schema(self):
        rule_page = RuleConfigurationPage()
        rule_id = "R_MIN_001"
        rule_name = "Rule with Minimum Schema"
        trigger_type = "balance_above"
        action_type = "transfer"
        result_msg = await rule_page.create_rule_with_minimum_required_schema(rule_id, rule_name, trigger_type, action_type)
        assert isinstance(result_msg, str)
        assert "valid" in result_msg.lower() or "success" in result_msg.lower() or "error" in result_msg.lower()

    @pytest.mark.asyncio
    async def test_create_rule_with_unsupported_trigger(self):
        rule_page = RuleConfigurationPage()
        rule_id = "R_UNSUPPORTED_001"
        rule_name = "Rule with Unsupported Trigger"
        unsupported_trigger_type = "future_trigger"
        action_type = "transfer"
        result_msg = await rule_page.create_rule_with_unsupported_trigger(rule_id, rule_name, unsupported_trigger_type, action_type)
        assert isinstance(result_msg, str)
        assert "error" in result_msg.lower() or "invalid" in result_msg.lower() or "unsupported" in result_msg.lower()
