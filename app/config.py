"""CONFIG FOR FLASK APP"""
import os
import dotenv

dotenv.load_dotenv()

class Config:
    """Base configuration."""
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    MODEL_ID = os.getenv('MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
    ALLOWED_ORIGINS = [
        origin.strip() for origin in os.getenv('ALLOWED_ORIGINS', '127.0.0.1:3000,localhost:3000').split(',')
    ]
    CAPTURED_ORIGIN = os.getenv('CAPTURED_ORIGIN', '*')

class LocalConfig(Config):
    """Local development configurations."""
    ENV = 'LOCAL'
    EMAIL = os.getenv('EMAIL', 'fname.lname@takeda.com')

class DevelopmentConfig(Config):
    """Development-specific configurations."""
    ENV = 'DEV'

class TestingConfig(Config):
    """Testing-specific configurations."""
    ENV = 'TEST'

class ProductionConfig(Config):
    """Production-specific configurations."""
    ENV = 'PROD'

config_by_name = {
    'DEV': DevelopmentConfig,
    'TEST': TestingConfig,
    'PROD': ProductionConfig,
    'LOCAL': LocalConfig,
}
