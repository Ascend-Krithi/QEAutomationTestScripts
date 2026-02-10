# Existing imports and class definition preserved
import time
import json
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    # ... [existing methods preserved] ...

    def attempt_rule_creation_with_injection(self, rule_payload, injection_type):
        """
        Attempts to create a rule with a specified injection payload and verifies API sanitization/rejection.
        Args:
            rule_payload (dict): The rule data with injection payload.
            injection_type (str): One of 'SQL', 'XSS', 'CMD'.
        Returns:
            dict: API response data.
        """
        # Assuming self.driver is Selenium WebDriver and self.api_url is set for API endpoint
        api_url = self.api_url + '/rules/create'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(rule_payload), headers=headers)
        result = {
            'status_code': response.status_code,
            'response_body': response.json() if response.content else {},
            'injection_type': injection_type
        }
        return result

    def verify_api_response_for_injection(self, response, expected_status=400):
        """
        Verifies that the API response matches expected sanitization/rejection criteria.
        Args:
            response (dict): API response from attempt_rule_creation_with_injection.
            expected_status (int): Expected HTTP status code.
        Returns:
            bool: True if response is as expected, False otherwise.
        """
        return response['status_code'] == expected_status

    def verify_security_audit_log_entry(self, rule_id, injection_type):
        """
        Verifies that a security audit log entry exists for the given rule_id and injection_type.
        Args:
            rule_id (str): Rule ID used in injection attempt.
            injection_type (str): 'SQL', 'XSS', or 'CMD'.
        Returns:
            bool: True if log entry found, False otherwise.
        """
        # Assuming audit log is accessible via API endpoint
        audit_url = self.api_url + '/security_audit_log'
        params = {'rule_id': rule_id, 'threat_type': 'injection_attempt'}
        response = requests.get(audit_url, params=params)
        if response.status_code != 200:
            return False
        logs = response.json()
        for log in logs:
            if log.get('rule_id') == rule_id and log.get('threat_type') == 'injection_attempt' and injection_type.lower() in log.get('payload', '').lower():
                return True
        return False

    def create_rule_with_maximum_triggers(self, rule_payload):
        """
        Creates a rule with the maximum allowed triggers (assumed limit is 10).
        Args:
            rule_payload (dict): Rule data with 10 triggers.
        Returns:
            dict: API response data.
        """
        api_url = self.api_url + '/rules/create'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(rule_payload), headers=headers)
        return {'status_code': response.status_code, 'response_body': response.json() if response.content else {}}

    def attempt_rule_creation_exceeding_triggers(self, rule_payload):
        """
        Attempts to create a rule exceeding the maximum triggers (e.g., 11).
        Args:
            rule_payload (dict): Rule data with 11 triggers.
        Returns:
            dict: API response data.
        """
        api_url = self.api_url + '/rules/create'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(rule_payload), headers=headers)
        return {'status_code': response.status_code, 'response_body': response.json() if response.content else {}}

    def create_rule_with_max_conditions_actions(self, rule_payload):
        """
        Creates a rule with maximum allowed conditions and actions (assumed limit is 20 each).
        Args:
            rule_payload (dict): Rule data with 20 conditions and 20 actions.
        Returns:
            dict: API response data.
        """
        api_url = self.api_url + '/rules/create'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(rule_payload), headers=headers)
        return {'status_code': response.status_code, 'response_body': response.json() if response.content else {}}

    def performance_validation(self, rule_id):
        """
        Measures response time for POST and GET operations on a rule to validate performance.
        Args:
            rule_id (str): Rule ID to test.
        Returns:
            dict: Contains response times for POST and GET.
        """
        api_url = self.api_url + '/rules/' + rule_id
        headers = {'Content-Type': 'application/json'}

        # Measure POST response time
        start_post = time.time()
        response_post = requests.post(api_url, headers=headers)
        end_post = time.time()
        post_time = end_post - start_post

        # Measure GET response time
        start_get = time.time()
        response_get = requests.get(api_url, headers=headers)
        end_get = time.time()
        get_time = end_get - start_get

        return {'post_time': post_time, 'get_time': get_time, 'post_status': response_post.status_code, 'get_status': response_get.status_code}

    # All new methods appended, existing logic unchanged.
