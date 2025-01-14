import unittest
from src.models.password_model import PasswordModel

class TestPasswordModel(unittest.TestCase):

    def setUp(self):
        self.password_model = PasswordModel(user_id=1, password_hash='hash', created_at='2023-01-01', updated_at='2023-01-01')

    def test_initialization(self):
        self.assertIsNotNone(self.password_model)

    def test_set_password(self):
        self.password_model.password_hash = "SecurePassword123!"
        self.assertEqual(self.password_model.password_hash, "SecurePassword123!")

    def test_get_password(self):
        self.password_model.password_hash = "AnotherSecurePassword!"
        self.assertEqual(self.password_model.password_hash, "AnotherSecurePassword!")

    def test_password_validation_data(self):
        self.password_model.password_hash = "ValidPassword!"
        self.password_model.validation_data = {"length": 14, "contains_special": True}
        self.assertEqual(self.password_model.validation_data, {"length": 14, "contains_special": True})

    def test_clear_password(self):
        self.password_model.password_hash = "ClearThisPassword!"
        self.password_model.password_hash = None
        self.assertIsNone(self.password_model.password_hash)

if __name__ == '__main__':
    unittest.main()