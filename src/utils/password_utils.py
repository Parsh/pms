import random
import string
import hashlib
import bcrypt

class PasswordUtils:
    def generate_password(self, policy):
        length = policy.get('min_length', 12)
        special_chars = policy.get('special_chars', '!@#$%^&*()')
        
        # Initialize with required characters
        password_chars = []
        if policy.get('require_lowercase', True):
            password_chars.append(random.choice(string.ascii_lowercase))
        if policy.get('require_uppercase', True):
            password_chars.append(random.choice(string.ascii_uppercase))
        if policy.get('require_numbers', True):
            password_chars.append(random.choice(string.digits))
        if policy.get('require_special_chars', True):
            password_chars.append(random.choice(special_chars))
            
        # Build character set for remaining length
        chars = ''
        if policy.get('require_lowercase', True):
            chars += string.ascii_lowercase
        if policy.get('require_uppercase', True):
            chars += string.ascii_uppercase
        if policy.get('require_numbers', True):
            chars += string.digits
        if policy.get('require_special_chars', True):
            chars += special_chars
            
        # Fill remaining length with random characters
        remaining_length = length - len(password_chars)
        password_chars.extend(random.choice(chars) for _ in range(remaining_length))
        
        # Shuffle the password characters
        random.shuffle(password_chars)
        return ''.join(password_chars)

    def hash_password(self, password):
        # Using bcrypt for secure password hashing
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def validate_password_policy(self, password, policy):
        if not password:
            return False

        if len(password) < policy.get('min_length', 8):
            return False

        if policy.get('require_uppercase') and not any(c.isupper() for c in password):
            return False

        if policy.get('require_lowercase') and not any(c.islower() for c in password):
            return False

        if policy.get('require_numbers') and not any(c.isdigit() for c in password):
            return False

        if policy.get('require_special_chars'):
            special_chars = '!@#$%^&*()'
            if not any(c in special_chars for c in password):
                return False

        return True

# Standalone function interfaces
def generate_password(policy):
    utils = PasswordUtils()
    return utils.generate_password(policy)

def hash_password(password):
    utils = PasswordUtils()
    return utils.hash_password(password)

def check_password(password, hashed_password):
    utils = PasswordUtils()
    return utils.check_password(password, hashed_password)

def validate_password_policy(password, policy):
    utils = PasswordUtils()
    return utils.validate_password_policy(password, policy)