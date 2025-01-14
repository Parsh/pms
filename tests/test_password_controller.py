import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import create_app

app = create_app()

import unittest
from flask import json

class TestPasswordController(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_generate_password(self):
        policy = {
            'min_length': 12,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special_chars': True
        }
        response = self.app.post('/api/generate', 
                               json={'policy': policy})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('password', data)
        self.assertIsInstance(data['password'], str)
        self.assertGreaterEqual(len(data['password']), 12)

    def test_validate_password(self):
        password = "Test@1234"
        response = self.app.post('/api/validate', json={'password': password})
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_valid', response.json)

    def test_validate_password_invalid(self):
        password = "1234"  # This should be invalid according to our policy
        response = self.app.post('/api/validate', json={'password': password})
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_valid', response.json)
        self.assertFalse(response.json['is_valid'])  # Should be false for invalid password

if __name__ == '__main__':
    unittest.main()