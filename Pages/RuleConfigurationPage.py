import asyncio
from typing import Any
from playwright.async_api import Page, Locator

class RuleConfigurationPage:
    """
    PageClass for Automated Transfers Rule Configuration.
    Supports rule creation, trigger/condition/action setup, and validation.
    Generated from Locators.json and test case analysis.
    """
    def __init__(self, page: Page):
        self.page = page
        # Rule form
        self.rule_id_input: Locator = page.locator("id=rule-id-field")
        self.rule_name_input: Locator = page.locator("name=rule-name")
        self.save_rule_button: Locator = page.locator("button[data-testid='save-rule-btn']")
        # Triggers
        self.trigger_type_dropdown: Locator = page.locator("id=trigger-type-select")
        self.date_picker: Locator = page.locator("input[type='date']")
        self.recurring_interval_input: Locator = page.locator("id=interval-value")
        self.after_deposit_toggle: Locator = page.locator("id=trigger-after-deposit")
        # Conditions
        self.add_condition_btn: Locator = page.locator("id=add-condition-link")
        self.condition_type_dropdown: Locator = page.locator("select.condition-type")
        self.balance_threshold_input: Locator = page.locator("input[name='balance-limit'")
        self.transaction_source_dropdown: Locator = page.locator("id=source-provider-select")
        self.operator_dropdown: Locator = page.locator("css=.condition-operator-select")
        # Actions
        self.action_type_dropdown: Locator = page.locator("id=action-type-select")
        self.transfer_amount_input: Locator = page.locator("name=fixed-amount")
        self.percentage_input: Locator = page.locator("id=deposit-percentage")
        self.destination_account_input: Locator = page.locator("id=target-account-id")
        # Validation
        self.json_schema_editor: Locator = page.locator("css=.monaco-editor")
        self.validate_schema_btn: Locator = page.locator("id=btn-verify-json")
        self.success_message: Locator = page.locator(".alert-success")
        self.schema_error_message: Locator = page.locator("[data-testid='error-feedback-text']")

    async def navigate_to_rule_creation(self, url: str):
        """Navigate to the rule creation interface."""
        await self.page.goto(url)
        await self.page.wait_for_selector("button[data-testid='save-rule-btn']")

    async def set_rule_id(self, rule_id: str):
        await self.rule_id_input.fill(rule_id)

    async def set_rule_name(self, rule_name: str):
        await self.rule_name_input.fill(rule_name)

    async def select_trigger_type(self, trigger_type: str):
        await self.trigger_type_dropdown.select_option(trigger_type)

    async def set_specific_date_trigger(self, date_str: str):
        await self.date_picker.fill(date_str)

    async def set_recurring_interval(self, interval_value: str):
        await self.recurring_interval_input.fill(interval_value)

    async def toggle_after_deposit(self, enable: bool):
        current_state = await self.after_deposit_toggle.is_checked()
        if enable != current_state:
            await self.after_deposit_toggle.click()

    async def add_condition(self):
        await self.add_condition_btn.click()

    async def select_condition_type(self, condition_type: str):
        await self.condition_type_dropdown.select_option(condition_type)

    async def set_balance_threshold(self, amount: Any):
        await self.balance_threshold_input.fill(str(amount))

    async def select_transaction_source(self, source: str):
        await self.transaction_source_dropdown.select_option(source)

    async def select_operator(self, operator: str):
        await self.operator_dropdown.select_option(operator)

    async def select_action_type(self, action_type: str):
        await self.action_type_dropdown.select_option(action_type)

    async def set_transfer_amount(self, amount: Any):
        await self.transfer_amount_input.fill(str(amount))

    async def set_percentage(self, percentage: Any):
        await self.percentage_input.fill(str(percentage))

    async def set_destination_account(self, account_id: str):
        await self.destination_account_input.fill(account_id)

    async def validate_schema(self):
        await self.validate_schema_btn.click()
        await self.page.wait_for_selector(".alert-success, [data-testid='error-feedback-text']")

    async def save_rule(self):
        await self.save_rule_button.click()
        await self.page.wait_for_selector(".alert-success")

    async def get_success_message(self) -> str:
        return await self.success_message.inner_text()

    async def get_schema_error_message(self) -> str:
        return await self.schema_error_message.inner_text()
