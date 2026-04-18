import pytest
from LoginPage import LoginPage

# Existing test methods...
@pytest.mark.asyncio
async def test_TC_LOGIN_009_invalid_login_rate_limiting(browser): ...
@pytest.mark.asyncio
async def test_TC_LOGIN_010_case_sensitivity_in_login(browser): ...
# ...
@pytest.mark.asyncio
async def test_TC_LOGIN_006_remember_me_session_persistence(browser): ...

@pytest.mark.asyncio
async def test_TC_LOGIN_001_successful_login(browser):
    login_page = LoginPage(browser)
    await login_page.validate_successful_login(
        url='https://example.com/login',
        email='user@example.com',
        password='ValidPass123'
    )

@pytest.mark.asyncio
async def test_TC_LOGIN_002_invalid_login(browser):
    login_page = LoginPage(browser)
    await login_page.validate_invalid_login(
        url='https://example.com/login',
        email='user@example.com',
        password='WrongPass456',
        expected_error='Invalid credentials'
    )
