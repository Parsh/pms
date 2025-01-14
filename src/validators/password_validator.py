from src.config import DEFAULT_PASSWORD_POLICY

class PasswordValidator:
    def __init__(self, policy=None):
        self.policy = policy if policy is not None else DEFAULT_PASSWORD_POLICY

    def validate(self, password):
        if not password:
            return False

        # Check minimum length
        if len(password) < self.policy.get('min_length', 12):
            return False

        # Check uppercase requirement
        if self.policy.get('require_uppercase') and not any(c.isupper() for c in password):
            return False

        # Check lowercase requirement
        if self.policy.get('require_lowercase') and not any(c.islower() for c in password):
            return False

        # Check numbers requirement - explicitly check for digits
        if self.policy.get('require_numbers', True) and not any(c.isdigit() for c in password):
            return False

        # Check special characters requirement - use policy-defined special chars
        if self.policy.get('require_special_chars', True):
            special_chars = self.policy.get('special_chars', '!@#$%^&*()')
            if not any(c in special_chars for c in password):
                return False

        return True

    def update_policy(self, new_policy):
        self.policy = new_policy