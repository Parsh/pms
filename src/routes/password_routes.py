import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Blueprint, request, jsonify
from controllers.password_controller import PasswordController

password_routes = Blueprint('password_routes', __name__)
controller = PasswordController()

@password_routes.route('/generate', methods=['POST'])
def generate_and_store_password():
    return controller.generate_and_store_password()

@password_routes.route('/validate', methods=['POST'])
def validate_password():
    return controller.validate_password()

@password_routes.route('/update_policy', methods=['POST'])
def update_policy():
    return controller.update_policy()

@password_routes.route('/validate_external', methods=['POST'])
def validate_external():
    return controller.validate_with_external_service()