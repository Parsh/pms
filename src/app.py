import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from src.routes.password_routes import password_routes

def create_app():
    app = Flask(__name__)

    # Register routes
    app.register_blueprint(password_routes, url_prefix='/api')

    # Additional middleware and configurations can be added here

    @app.route('/')
    def index():
        return "Welcome to the Password Management System"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)