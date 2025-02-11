import unittest
from src.models.password_model import PasswordModel

class TestPasswordModel(unittest.TestCase):
    def setUp(self):
        self.password_model = PasswordModel(
            user_id=1, 
            password_hash='hash', 
            created_at='2023-01-01', 
            updated_at='2023-01-01',
            policy_number=1
        )

    def test_initialization(self):
        self.assertEqual(self.password_model.user_id, 1)
        self.assertEqual(self.password_model.password_hash, 'hash')
        self.assertEqual(self.password_model.created_at, '2023-01-01')
        self.assertEqual(self.password_model.updated_at, '2023-01-01')
        self.assertEqual(self.password_model.policy_number, 1)

    def test_clear_password(self):
        self.password_model.password_hash = None
        self.assertIsNone(self.password_model.password_hash)

    def test_get_password(self):
        self.assertEqual(self.password_model.password_hash, 'hash')

    def test_set_password(self):
        self.password_model.password_hash = 'new_hash'
        self.assertEqual(self.password_model.password_hash, 'new_hash')

    def test_password_validation_data(self):
        data = self.password_model.to_dict()
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['password_hash'], 'hash')
        self.assertEqual(data['created_at'], '2023-01-01')
        self.assertEqual(data['updated_at'], '2023-01-01')
        self.assertEqual(data['policy_number'], 1)

if __name__ == '__main__':
    unittest.main()