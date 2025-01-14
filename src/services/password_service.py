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
        self.policy = {'min_length': 8}
        self.password_utils = PasswordUtils()
        self.password_validator = PasswordValidator(DEFAULT_PASSWORD_POLICY)
        self.storage_file = 'passwords.json'

    def generate_password(self, policy=None):
        if policy is None:
            policy = self.policy
            
        characters = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(secrets.choice(characters) for _ in range(policy['min_length']))
            if self.validate_password(password):
                return password

    def validate_password(self, password):
        if len(password) < self.policy.get('min_length', 8):
            return False
        if self.policy.get('require_uppercase') and not any(c.isupper() for c in password):
            return False
        if self.policy.get('require_lowercase') and not any(c.islower() for c in password):
            return False
        if self.policy.get('require_numbers') and not any(c.isdigit() for c in password):
            return False
        if self.policy.get('require_special_chars') and not any(c in string.punctuation for c in password):
            return False
        return True

    def update_policy(self, new_policy):
        self.policy.update(new_policy)
        self.password_validator.update_policy(new_policy)

    def check_password_breach(self, password):
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        return suffix in response.text

    def store_password(self, user_id, password):
        if not user_id or not password:
            raise ValueError("User ID and password are required")
        hashed_password = self.password_utils.hash_password(password)
        now = datetime.now().isoformat()
        
        password_data = {
            'user_id': user_id,
            'password_hash': hashed_password,
            'created_at': now,
            'updated_at': now
        }

        # Load existing data
        all_passwords = self._load_passwords()
        all_passwords[user_id] = password_data
        
        # Save to file
        self._save_passwords(all_passwords)
        return True

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

    def hash_password(self, password):
        return self.password_utils.hash_password(password)

    def check_password(self, password, hashed_password):
        return self.password_utils.check_password(password, hashed_password)

    def verify_stored_password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)