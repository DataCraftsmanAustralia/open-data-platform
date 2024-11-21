import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from a .env file if it exists
load_dotenv()

class Config:
    # Flask settings   
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Mail settings (if you're sending emails)
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False').lower() == 'true'
    EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    
    POSTGRES_URL = os.environ.get('DATABASE')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE')

    
class DevelopmentConfig(Config):
    # Add any development-specific settings here
    DEBUG = True        

class ProductionConfig(Config):
    # Add any production-specific settings here
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}