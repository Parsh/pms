from flask import jsonify, request
from src.services.password_service import PasswordService

class PasswordController:
    def __init__(self):
        self.password_service = PasswordService()

    def generate_password(self):
        try:
            policy = request.json.get('policy', {})
            if not policy:
                policy = {
                    'min_length': 12,
                    'require_uppercase': True,
                    'require_lowercase': True,
                    'require_numbers': True,
                    'require_special_chars': True
                }
            
            password = self.password_service.generate_password(policy)
            return jsonify({'password': password}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def validate_password(self):
        try:
            password = request.json.get('password')
            if not password:
                return jsonify({'error': 'Password is required'}), 400
            is_valid = self.password_service.validate_password(password)
            return jsonify({'is_valid': is_valid}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def change_policy(self):
        new_policy = request.json.get('policy')
        self.password_service.update_policy(new_policy)
        return jsonify({'message': 'Password policy updated successfully'}), 200

    def store_password(self):
        try:
            user_id = request.json.get('user_id')
            password = request.json.get('password')
            if not user_id or not password:
                return jsonify({'error': 'User ID and password are required'}), 400
            self.password_service.store_password(user_id, password)
            return jsonify({'message': 'Password stored successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def validate_with_external_service(self):
        try:
            password = request.json.get('password', '')
            if not password:
                return jsonify({'error': 'Password is required'}), 400
            is_breached = self.password_service.check_password_breach(password)
            return jsonify({'is_breached': is_breached}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500