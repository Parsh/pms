# Password Management System

## Overview
The Password Management System is a secure application designed to generate, validate, and manage passwords according to defined policies. It follows a structured development approach to ensure software security, implementing a "shift-left" strategy to address security concerns early in the development lifecycle.

## Features
- Password generation based on customizable policies.
- Secure storage and validation of password data.
- Integration with external services for enhanced security (e.g., HIPB for breach detection).
- RESTful API for interaction with third-party applications.

## Project Structure
```
password-management-system
├── src
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── controllers
│   │   ├── __init__.py
│   │   └── password_controller.py
│   ├── models
│   │   ├── __init__.py
│   │   └── password_model.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── password_routes.py
│   ├── services
│   │   ├── __init__.py
│   │   └── password_service.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── password_utils.py
│   └── validators
│       ├── __init__.py
│       └── password_validator.py
├── tests
│   ├── __init__.py
│   ├── test_password_controller.py
│   ├── test_password_model.py
│   ├── test_password_service.py
│   ├── test_password_utils.py
│   └── test_password_validator.py
├── requirements.txt
├── setup.py
└── README.md
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/password-management-system.git
cd password-management-system
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python src/app.py
```

### 5. Access the Application
Open your web browser and go to `http://127.0.0.1:5000` to see the welcome message.

## Configuration

### Password Policy Configuration
Default password policies can be modified in `config.py`:
```python
PASSWORD_POLICY = {
    'min_length': 12,
    'max_length': 128,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special_chars': True,
    'special_chars': '!@#$%^&*()_+-=[]{}|;:,.<>?'
}
```

## API Endpoints

### Generate and Store Password
- **URL:** `/api/generate`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "user_id": "user_id"
  }
  ```
- **Response:**
  ```json
  {
  "password": "generated_password",
  }
  ```

### Validate Password
- **URL:** `/api/validate`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "user_id": "user_id",
    "password": "password_to_validate"
  }
  ```
- **Response:**
  ```json
  {
    "is_valid": true
  }
  ```

### Validate with External Service
- **URL:** `/api/validate_external`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "password": "password_to_validate"
  }
  ```
- **Response:**
  ```json
  {
    "is_valid": true
  }
  ```

### Update Policy (Admin Only)
- **URL:** `/api/update_policy`
- **Method:** `POST`
- **Payload:**
  ```json
  {
  "policy": {
    "min_length": 12,
    "require_uppercase": true,
    "require_lowercase": true,
    "require_numbers": true,
    "require_special_chars": true
   }
  }
  ```
- **Response:**
  ```json
  {
  "message": "Password policy updated successfully"
  }
  ```

## Logging and Monitoring
- Application logs are stored in `logs/app.log`
- Monitoring metrics are exposed at `/metrics` endpoint
- Integration with standard monitoring tools (Prometheus/Grafana) is supported

## System Requirements
- Python 3.8 or higher
- PostgreSQL 12+
- Memory: 512MB minimum
- Disk space: 1GB recommended

## Testing
Unit tests are provided to ensure the functionality of the application. To run the tests, use:
```
pytest tests/
```

## Security Considerations
- Passwords are securely hashed and stored.
- The application adheres to defined password policies, which can be updated as needed.
- Regular static code analysis is performed to identify potential vulnerabilities.

## License
This project is licensed under the MIT License. See the LICENSE file for details.