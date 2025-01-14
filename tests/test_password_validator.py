import unittest
from src.validators.password_validator import PasswordValidator

class TestPasswordValidator(unittest.TestCase):
    def setUp(self):
        self.validator = PasswordValidator({
            'min_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special_chars': True,
            'special_chars': '!@#$%^&*()'
        })

    def test_valid_password(self):
        password = "StrongP@ssw0rd!"
        self.assertTrue(self.validator.validate(password))

    def test_invalid_password_too_short(self):
        password = "Short1!"
        self.assertFalse(self.validator.validate(password))

    def test_invalid_password_no_uppercase(self):
        password = "lowercase1!"
        self.assertFalse(self.validator.validate(password))

    def test_invalid_password_no_digit(self):
        password = "NoDigit!"  # Missing number
        self.assertFalse(self.validator.validate(password))

    def test_invalid_password_no_special_char(self):
        password = "NoSpecial123"  # Missing special character
        self.assertFalse(self.validator.validate(password))

    def test_policy_change_impact(self):
        self.validator.policy = {'min_length': 12, 'require_special': True}
        password = "NewPolicy1!"
        self.assertFalse(self.validator.validate(password))

        password = "NewPolicy123!"
        self.assertTrue(self.validator.validate(password))

if __name__ == '__main__':
    unittest.main()