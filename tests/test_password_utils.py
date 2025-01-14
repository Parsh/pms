import pytest
from src.utils.password_utils import generate_password, validate_password_policy

def test_generate_password():
    policy = {
        'min_length': 12,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special_chars': True
    }
    password = generate_password(policy)
    assert len(password) >= 12
    assert any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in '!@#$%^&*()' for c in password)

def test_validate_password_policy():
    policy = {
        'min_length': 12,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special_chars': True
    }
    assert validate_password_policy('Ab1!defghijkl', policy) == True
    assert validate_password_policy('abcdefghijkl', policy) == False  # no uppercase
    assert validate_password_policy('ABCDEFGHIJKL', policy) == False  # no lowercase
    assert validate_password_policy('Abcdefghijkl', policy) == False  # no number
    assert validate_password_policy('Ab1defghijkl', policy) == False  # no special char