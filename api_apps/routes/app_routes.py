from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_apps import Logger
from flasgger import swag_from

class AppRoutes(Blueprint):
    def __init__(self, app_service, app_schema):
        # Initialize the blueprint, logger, and service schema
        super().__init__('apps', __name__)
        self.app_service = app_service
        self.app_schema = app_schema
        self.register_routes()  # Register all the routes
        self.logger = Logger()

    def register_routes(self):
        # Define all API endpoints for the application
        self.route('/api/v1/apps', methods=['GET'])(self.get_apps)
        self.route('/api/v1/apps', methods=['POST'])(self.add_app)
        self.route('/api/v1/apps/<int:app_id>', methods=['PUT'])(self.update_app)
        self.route('/api/v1/apps/<int:app_id>', methods=['DELETE'])(self.delete_app)
        self.route('/api/v1/apps/<int:app_id>', methods=['GET'])(self.get_app_by_id)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)
        self.route('/api/v1/apps/<string:name>', methods=['GET'])(self.get_app_by_name)

    @swag_from({
        'tags': ['Apps'],  # Swagger tag to group endpoints
        'responses': {
            200: {
                'description': 'List of all apps'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def get_apps(self):
        try:
            # Fetch all apps using the service
            apps = self.app_service.get_all_apps()
            return jsonify(apps), 200
        except Exception as e:
            # Log an error if fetching fails
            self.logger.error(f'Error fetching apps: {e}')
            return jsonify({'error': f'Error fetching apps: {e}'}), 500

    @swag_from({
        'tags': ['Apps'],
        'parameters': [
            {
                'name': 'body',  # Input parameter type
                'in': 'body',  # Passed in the request body
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'info': {'type': 'string'},
                        'description': {'type': 'string'},
                        'url': {'type': 'string'},
                        'logo_url': {'type': 'string'},
                        'origin': {'type': 'string'},
                        'author': {'type': 'string'}
                    },
                    'required': ['name', 'url']  # Mandatory fields
                }
            }
        ],
        'responses': {
            201: {
                'description': 'App successfully created'
            },
            400: {
                'description': 'Invalid data or app already exists'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def add_app(self):
        try:
            # Parse and validate the request body
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 401

            try:
                # Validate the input schema using Marshmallow
                self.app_schema.load(request_data)
            except ValidationError as e:
                return jsonify({'error': f'Validation failed: {e.messages}'}), 400

            # Call the service to add the app
            service_response = self.app_service.add_app(request_data)

            # If the service response is already a Response object, return it
            if isinstance(service_response, tuple):
                return service_response

            # Log successful creation and return the response
            self.logger.info(f'App created: {service_response}')
            return jsonify(service_response), 201
        except Exception as e:
            # Log and handle unexpected errors
            self.logger.error(f'Error creating app: {e}')
            return jsonify({'error': f'Error creating app: {e}'}), 500


    @swag_from({
        'tags': ['Apps'],
        'parameters': [
            {
                'name': 'app_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'App ID to be updated'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'info': {'type': 'string'},
                        'description': {'type': 'string'},
                        'url': {'type': 'string'},
                        'logo_url': {'type': 'string'},
                        'origin': {'type': 'string'},
                        'author': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'App successfully updated'
            },
            400: {
                'description': 'Invalid data or app not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def update_app(self, app_id):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 403

            try:
                # Validate only the fields provided in the request (partial update)
                self.app_schema.load(request_data, partial=True)
            except ValidationError as e:
                return jsonify({'error': f'Validation failed: {e.messages}'}), 405

            updated_app = self.app_service.update_app(app_id, request_data)
            if updated_app is None:
                return jsonify({'error': 'App not found'}), 404

            return jsonify({'message': 'App successfully updated', 'app': updated_app}), 201
        except Exception as e:
            self.logger.error(f'Error updating app: {e}')
            return jsonify({'error': f'Error updating app: {e}'}), 501


    @swag_from({
        'tags': ['Apps'],
        'parameters': [
            {
                'name': 'app_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'App ID to be deleted'
            }
        ],
        'responses': {
            200: {
                'description': 'App successfully deleted'
            },
            400: {
                'description': 'App not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def delete_app(self, app_id):
        try:
            # Delete the app using the service
            result = self.app_service.delete_app(app_id)
            if result is None:
                return jsonify({'error': 'App not found'}), 404

            return jsonify({'message': 'App successfully deleted', 'app': result}), 202
        except Exception as e:
            self.logger.error(f'Error deleting app: {e}')
            return jsonify({'error': f'Error deleting app: {e}'}), 505

    @swag_from({
        'tags': ['Apps'],
        'parameters': [
            {
                'name': 'app_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'App ID to retrieve'
            }
        ],
        'responses': {
            200: {
                'description': 'App successfully retrieved'
            },
            400: {
                'description': 'App not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def get_app_by_id(self, app_id):
        try:
            # Fetch the app by ID using the service
            app = self.app_service.get_app_by_id(app_id)
            if app is None:
                return jsonify({'error': 'App not found'}), 404

            return jsonify(app), 200
        except Exception as e:
            self.logger.error(f'Error fetching app by ID: {e}')
            return jsonify({'error': f'Error fetching app by ID: {e}'}), 506

    @swag_from({
        'tags': ['Apps'],
        'parameters': [
            {
                'name': 'name',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'Name of the app to retrieve'
            }
        ],
        'responses': {
            200: {
                'description': 'App successfully retrieved'
            },
            400: {
                'description': 'App not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def get_app_by_name(self, name):
        try:
            # Fetch the app by name using the service
            app = self.app_service.get_app_by_name(name)
            if app is None:
                return jsonify({'error': 'App not found'}), 404

            return jsonify(app), 200
        except Exception as e:
            self.logger.error(f'Error fetching app by name: {e}')
            return jsonify({'error': f'Error fetching app by name: {e}'}), 507

    def healthcheck(self):
        # Healthcheck endpoint to verify service is running
        return jsonify({'status': 'up'}), 200
