from flask import Flask, request, redirect, url_for, g, session
from config import config

import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'production')
    
    app.config.from_object(config[config_name])
   

    # Register blueprints       
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

    