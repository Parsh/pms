# Configuration settings for the password management system

import os

DEFAULT_PASSWORD_POLICY = {
    'min_length': 12,
    'max_length': 128,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special_chars': True,
    'special_chars': '!@#$%^&*()'
}

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    PASSWORD_POLICY = {
        'min_length': 8,
        'max_length': 20,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special_characters': True,
    }
    # Add other configuration settings as needed

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Configuration mapping
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}