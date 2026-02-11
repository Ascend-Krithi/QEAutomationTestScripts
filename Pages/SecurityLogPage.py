# SecurityLogPage.py
"""
PageClass for verifying security log entries related to SQL injection attempts.
"""

import os

class SecurityLogPage:
    def __init__(self, log_path='/var/log/security/injection_attempts.log'):
        self.log_path = log_path

    def verify_injection_attempt_logged(self, search_string):
        if not os.path.exists(self.log_path):
            return False
        with open(self.log_path, 'r') as log_file:
            for line in log_file:
                if search_string in line:
                    return True
        return False
