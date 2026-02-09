from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    ...
    # [existing code unchanged]

    # --- Appended for TC-FT-009 & TC-FT-010 ---
    def create_rule_with_empty_conditions(self, rule_json):
        """
        Creates a rule with an empty conditions array and verifies success.
        Args:
            rule_json: Rule JSON with empty conditions.
        Returns:
            Success message or error.
        """
        self.open_rule_form()
        # Fill rule fields
        if 'ruleId' in rule_json:
            self.set_rule_id(rule_json['ruleId'])
        if 'ruleName' in rule_json:
            self.set_rule_name(rule_json['ruleName'])
        trigger = rule_json.get('trigger', {})
        action = rule_json.get('action', {})
        # Trigger setup
        trigger_type = trigger.get('type')
        if trigger_type == 'specific_date':
            self.set_specific_date_trigger(trigger.get('date', ''))
        elif trigger_type == 'after_deposit':
            self.set_after_deposit_trigger()
        else:
            return f"Unsupported trigger type: {trigger_type}"
        # Action setup
        if action.get('type') == 'fixed_amount':
            self.set_fixed_amount_action(action.get('amount', ''))
        # No conditions to add
        self.save_rule()
        return self.validate_schema()

    def retrieve_rule(self, rule_id):
        """
        Retrieves a rule from backend by rule_id and returns its details.
        Args:
            rule_id: Rule identifier.
        Returns:
            Dict with rule details or error message.
        """
        try:
            rules_list = self.driver.find_elements(By.CSS_SELECTOR, '.rule-list-item')
            for rule in rules_list:
                if rule_id in rule.text:
                    rule.click()
                    # Example: Fetch rule details from UI
                    details = self.driver.find_element(By.CSS_SELECTOR, '.rule-details')
                    return details.text
            return f"Rule {rule_id} not found."
        except Exception as e:
            return f"Error retrieving rule: {str(e)}"

    def trigger_rule_with_empty_conditions(self, trigger_data):
        """
        Triggers a rule with empty conditions and validates unconditional execution.
        Args:
            trigger_data: Dict with trigger info (e.g., deposit amount).
        Returns:
            Confirmation message or error.
        """
        try:
            if 'deposit' in trigger_data:
                confirmation = self.simulate_deposit(trigger_data['deposit'])
                return confirmation
            # Add other triggers if needed
            return "Trigger type not supported for simulation."
        except Exception as e:
            return f"Error triggering rule: {str(e)}"

    def validate_unconditional_transfer(self, expected_amount):
        """
        Validates that transfer is executed without conditions.
        Args:
            expected_amount: Amount expected to be transferred.
        Returns:
            True if transfer found, False otherwise.
        """
        try:
            transaction_logs = self.driver.find_elements(By.CSS_SELECTOR, '.transaction-log-item')
            for log in transaction_logs:
                if str(expected_amount) in log.text:
                    return True
            return False
        except Exception:
            return False
