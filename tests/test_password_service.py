import unittest
from unittest.mock import Mock, patch
from src.services.password_service import PasswordService
from src.models.password_model import PasswordModel
from src.validators.password_validator import PasswordValidator
from src.utils.password_utils import PasswordUtils

class TestPasswordService(unittest.TestCase):
    def setUp(self):
        self.password_service = PasswordService()

    def test_generate_and_store_password(self):
        user_id = "test_user_123"
        password, policy_number = self.password_service.generate_password()
        self.assertIsNotNone(password)
        self.assertGreaterEqual(len(password), 8)
        self.assertEqual(policy_number, self.password_service.current_policy_number)
        self.assertTrue(self.password_service.store_password(user_id, password))

    def test_validate_password(self):
        user_id = "test_user_123"
        password = "TestPass123!"
        self.password_service.store_password(user_id, password)
        is_valid, message = self.password_service.validate_password(user_id, password)
        self.assertTrue(is_valid)
        self.assertIsNone(message)

    def test_validate_password_policy_mismatch(self):
        user_id = "test_user_123"
        password = "TestPass123!"
        self.password_service.store_password(user_id, password)
        self.password_service.update_policy({'min_length': 12})
        is_valid, message = self.password_service.validate_password(user_id, password)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Password policy mismatch. Please update your password.")

    def test_change_password_policy(self):
        new_policy = {
            'min_length': 12,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special_chars': True
        }
        self.password_service.update_policy(new_policy)
        # Test with valid password
        self.assertTrue(self.password_service.validate_password("test_user_123", "TestPass123!"))

    def test_hibp_integration(self):
        with patch('src.services.password_service.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = ""  # Simulating no breaches
            result = self.password_service.check_password_breach("TestPass123!")
            self.assertFalse(result)

    def test_password_persistence(self):
        user_id = "test_user_123"
        password = "TestPass123!"
        self.assertTrue(self.password_service.store_password(user_id, password))
        stored_data = self.password_service.retrieve_password_data(user_id)
        self.assertIsNotNone(stored_data)
        self.assertTrue(self.password_service.password_utils.check_password(password, stored_data['password_hash']))

    def test_policy_change_validation(self):
        initial_policy = {'min_length': 8}
        self.password_service.update_policy(initial_policy)
        password, _ = self.password_service.generate_password()
        
        # Change policy and verify previous password fails
        strict_policy = {
            'min_length': 12,
            'require_uppercase': True,
            'require_special_chars': True
        }
        self.password_service.update_policy(strict_policy)
        self.assertFalse(self.password_service.validate_password("test_user_123", password))

if __name__ == '__main__':
    unittest.main()