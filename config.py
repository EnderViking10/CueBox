import os

class Config:
    """Base configuration."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')  # Replace with a secure key
    DEBUG = False
    TESTING = False
    HOST = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')  # Default host
    PORT = int(os.environ.get('FLASK_RUN_PORT', 5000))  # Default port

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///cuebox.db')  # Use SQLite by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_cuebox.db'


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///cuebox.db')
