import json
import os
from datetime import datetime
from src.utils.password_utils import PasswordUtils
from src.validators.password_validator import PasswordValidator
from src.config import DEFAULT_PASSWORD_POLICY
import hashlib
import requests
import secrets
import string
import bcrypt

class PasswordService:
    def __init__(self):
        self.policy = DEFAULT_PASSWORD_POLICY
        self.password_utils = PasswordUtils()
        self.password_validator = PasswordValidator(DEFAULT_PASSWORD_POLICY)
        self.storage_file = 'passwords.json'
        self.policy_file = 'policies.json'
        self.current_policy_number = self._get_current_policy_number()

    def _get_current_policy_number(self):
        if not os.path.exists(self.policy_file):
            return 1
        with open(self.policy_file, 'r') as f:
            policies = json.load(f)
            return max(policies.keys(), default=1)

    def generate_password(self):
        password = self.password_utils.generate_password(self.policy)
        return password, self.current_policy_number

    def store_password(self, user_id, password):
        if not user_id or not password:
            raise ValueError("User ID and password are required")
        hashed_password = self.password_utils.hash_password(password)
        now = datetime.now().isoformat()
        
        password_data = {
            'user_id': user_id,
            'password_hash': hashed_password,
            'created_at': now,
            'updated_at': now,
            'policy_number': self.current_policy_number
        }

        # Load existing data
        all_passwords = self._load_passwords()
        all_passwords[user_id] = password_data
        
        # Save to file
        self._save_passwords(all_passwords)
        return True

    def validate_password(self, user_id, password):
        stored_data = self.retrieve_password_data(user_id)
        if not stored_data:
            return False, "User not found"

        stored_policy_number = stored_data.get('policy_number')
        if stored_policy_number != self.current_policy_number:
            return False, "Password policy mismatch. Please update your password."

        return self.password_utils.check_password(password, stored_data['password_hash']), None

    def update_policy(self, new_policy):
        self.policy.update(new_policy)
        self.password_validator.update_policy(new_policy)
        self.current_policy_number = int(self.current_policy_number) + 1
        self._save_policy(new_policy, self.current_policy_number)

    def _save_policy(self, policy, policy_number):
        if not os.path.exists(self.policy_file):
            policies = {}
        else:
            with open(self.policy_file, 'r') as f:
                policies = json.load(f)
        policies[policy_number] = policy
        with open(self.policy_file, 'w') as f:
            json.dump(policies, f, indent=4)

    def check_password_breach(self, password):
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        return suffix in response.text

    def retrieve_password_data(self, user_id):
        all_passwords = self._load_passwords()
        return all_passwords.get(user_id)

    def _load_passwords(self):
        if not os.path.exists(self.storage_file):
            return {}
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_passwords(self, data):
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=4)
