from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_users import Logger
from flasgger import swag_from

class UserRoutes(Blueprint):
    def __init__(self, user_service, user_schema):
        super().__init__('user', __name__)
        self.user_service = user_service
        self.user_schema = user_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/api/v1/users', methods=['GET'])(self.get_users)
        self.route('/api/v1/users', methods=['POST'])(self.add_user)
        self.route('/api/v1/users/<int:user_id>', methods=['PUT'])(self.update_user)
        self.route('/api/v1/users/<int:user_id>', methods=['DELETE'])(self.delete_user)
        self.route('/api/v1/users/<int:user_id>', methods=['GET'])(self.get_user_by_id)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Users'],
        'responses': {
            200: {
                'description': 'List of all users'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def get_users(self):
        try:
            users = self.user_service.get_all_users()
            return jsonify(users), 200
        except Exception as e:
            self.logger.error(f'Error fetching users: {e}')
            return jsonify({'error': f'Error fetching users: {e}'}), 500

    @swag_from({
        'tags': ['Users'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {'type': 'string'},
                        'password': {'type': 'string'}
                    },
                    'required': ['email', 'password']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'User successfully created'
            },
            400: {
                'description': 'Invalid data or user already exists'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def add_user(self):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400

            email = request_data.get('email')
            password = request_data.get('password')

            try:
                self.user_schema.validate_email(email)
                self.user_schema.validate_password(password)
            except ValidationError as e:
                return jsonify({'error': f'Validation failed: {e}'}), 400

            user_exists = self.user_service.check_user_exists(email)
            if user_exists:
                return jsonify({'error': 'User already exists'}), 400

            new_user = {
                'email': email,
                'password': password
            }
            created_user = self.user_service.add_user(new_user)
            self.logger.info(f'User created: {created_user}')
            return jsonify(created_user), 201
        except Exception as e:
            self.logger.error(f'Error creating user: {e}')
            return jsonify({'error': f'Error creating user: {e}'}), 500

    @swag_from({
        'tags': ['Users'],
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'User ID to be updated'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {'type': 'string'},
                        'password': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'User successfully updated'
            },
            400: {
                'description': 'Invalid data or user does not exist'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def update_user(self, user_id):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400

            email = request_data.get('email')
            password = request_data.get('password')

            if email:
                try:
                    self.user_schema.validate_email(email)
                except ValidationError as e:
                    return jsonify({'error': f'Validation failed: {e}'}), 400

            if password:
                try:
                    self.user_schema.validate_password(password)
                except ValidationError as e:
                    return jsonify({'error': f'Validation failed: {e}'}), 400

            updated_user = {k: v for k, v in request_data.items() if v is not None}

            result = self.user_service.update_user(user_id, updated_user)
            if result is None:
                return jsonify({'error': 'User does not exist'}), 400

            if isinstance(result, str):
                return jsonify({'message': result}), 200

            return jsonify({'message': 'User successfully updated', 'user': result}), 200
        except Exception as e:
            self.logger.error(f'Error updating user: {e}')
            return jsonify({'error': f'Error updating user: {e}'}), 500

    @swag_from({
        'tags': ['Users'],
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'User ID to be deleted'
            }
        ],
        'responses': {
            200: {
                'description': 'User successfully deleted'
            },
            400: {
                'description': 'User does not exist'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def delete_user(self, user_id):
        try:
            user = self.user_service.delete_user(user_id)
            if user is None:
                return jsonify({'error': 'User does not exist'}), 400

            return jsonify({'message': 'User successfully deleted', 'user': user}), 200
        except Exception as e:
            self.logger.error(f'Error deleting user: {e}')
            return jsonify({'error': f'Error deleting user: {e}'}), 500

    @swag_from({
        'tags': ['Users'],
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'User ID to retrieve'
            }
        ],
        'responses': {
            200: {
                'description': 'User successfully retrieved'
            },
            400: {
                'description': 'User does not exist'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def get_user_by_id(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            if user is None:
                return jsonify({'error': 'User does not exist'}), 400

            return jsonify(user), 200
        except Exception as e:
            self.logger.error(f'Error fetching user by ID: {e}')
            return jsonify({'error': f'Error fetching user by ID: {e}'}), 500


    def healthcheck(self):
        return jsonify({'status': 'up'}), 200