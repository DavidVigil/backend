from flask import Blueprint, jsonify, request
from logger.logger_apps import Logger
from marshmallow import ValidationError

class AppsRoutes(Blueprint):
    def __init__(self,App_service, app_schema):
        super().__init__('user_routes', __name__)
        self.app_service = App_service
        self.app_schema = app_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/apps/v1/apps', methods=['GET'])(self.get_apps)

    def get_apps(self):
        apps = self.apps_service.get_all_users()
        return jsonify(apps), 200

    def add_app(self):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400
            
            title = request_data.get('title')
            info = request_data.get('info')
            description = request_data.get('description')
            logo = request_data.get('logo')
            url = request_data.get('url')
            source = request_data.get('source')

            try:
                self.apps_schema.validate_title(title)
                self.apps_schema.validate_title(info)
                self.apps_schema.validate_title(description)
                self.apps_schema.validate_title(logo)
                self.apps_schema.validate_title(url)
                self.apps_schema.validate_title(source)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'})
            
            new_app = {
                'title' : title,
                'info' : info,
                'description' : description,
                'logo' : logo,
                'url' : url,
                'source' : source
            }
            created_app = self.apps_service.add_app(new_app)
            self.logger.info(f'New app: {created_app}')
            return jsonify(created_app), 201
        
        except Exception as e:
            self.logger.error(f'Error adding a new app to the database: {e}')
            return jsonify({'error': f'An error has ocurred: {e}'})
        
    def update_app(self, app_id):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400

            title = request_data.get('title')
            info = request_data.get('info')
            description = request_data.get('description')
            logo = request_data.get('logo')
            url = request_data.get('url')
            source = request_data.get('source')

            try:
                self.book_schema.validate_title(title)
                self.apps_schema.validate_title(info)
                self.apps_schema.validate_title(description)
                self.apps_schema.validate_title(logo)
                self.apps_schema.validate_title(url)
                self.apps_schema.validate_title(source)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'})

            update_book = {
                '_id': app_id,
                'info' : info,
                'description' : description,
                'logo' : logo,
                'url' : url,
                'source' : source
            }
            updated_app = self.app_service.update_book(app_id, updated_app)
            if updated_app:
                return jsonify(updated_app), 200
            else:
                return jsonify({'error': 'App not found'}), 404

        except  Exception as e:
            self.logger.error(f'Error updating the app in the database: {e}')
            return jsonify({'error': f'Error updating the app in the database: {e}'})

    def delete_app(self, app_id):
        try:
            deleted_app = self.app_service.delete_app(app_id)

            if deleted_app:
                return jsonify(deleted_app), 200
            else:
                return jsonify({'error: ': 'App Not Found'}), 404

        except Exception as e:
            self.logger.error(f'Error deleting the App from the database: {e}')
            return jsonify({'error: ': f'Error deleting the App from the database: {e}'})


    def healthcheck(self):
        return jsonify({'status': 'up'}), 200