"""Configuration classes for the HBnB application."""

import os


class DevelopmentConfig:
    """Development configuration."""
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hbnb-dev-secret-2024')


class TestingConfig:
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'hbnb-test-secret'


class ProductionConfig:
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')


config = {
    'development': DevelopmentConfig,
    'testing':     TestingConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}

