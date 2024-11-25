from flask import jsonify
from logger.logger_apps import Logger

class AppService:
    def __init__(self, db_conn):
        # Initialize the logger and the database connection
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_apps(self):
        try:
            # Retrieve all apps from the database
            apps = list(self.db_conn.db.apps.find({})) 
            return apps
        except Exception as e:
            # Log an error if the retrieval fails
            self.logger.error(f'Error fetching all apps from the database: {e}')
            return jsonify({'error': f'Error fetching all apps from the database: {e}'}), 500

    def check_app_exists(self, name):
        try:
            # Check if an app with the given name exists in the database
            app = self.db_conn.db.apps.find_one({'name': name})
            return app is not None
        except Exception as e:
            # Log an error if the check fails
            self.logger.error(f'Error checking if app exists: {e}')
            raise

    def add_app(self, new_app):
        try:
            # Verify if the app already exists
            if self.check_app_exists(new_app['name']):
                return jsonify({'error': 'App already exists'}), 400

            # Find the last app ID and calculate the next ID
            last_app = self.db_conn.db.apps.find_one(sort=[('_id', -1)])
            next_id = (last_app['_id'] + 1) if last_app else 1
            new_app['_id'] = next_id

            # Insert the new app into the database
            self.db_conn.db.apps.insert_one(new_app)
            return new_app
        except Exception as e:
            # Log an error if the insertion fails
            self.logger.error(f'Error creating the new app: {e}')
            return jsonify({'error': f'Error creating the new app: {e}'}), 500

    def get_app_by_id(self, app_id):
        try:
            # Retrieve the app by its unique ID
            app = self.db_conn.db.apps.find_one({'_id': app_id})
            return app
        except Exception as e:
            # Log an error if the retrieval fails
            self.logger.error(f'Error fetching the app by ID from the database: {e}')
            return jsonify({'error': f'Error fetching the app by ID from the database: {e}'}), 500

    def get_app_by_name(self, name):
        try:
            # Retrieve the app by its name
            app = self.db_conn.db.apps.find_one({'name': name})
            return app
        except Exception as e:
            # Log an error if the retrieval fails
            self.logger.error(f'Error fetching the app by name from the database: {e}')
            return jsonify({'error': f'Error fetching the app by name from the database: {e}'}), 500

    def update_app(self, app_id, updated_app):
        try:
            # Check if the app exists before updating
            existing_app = self.get_app_by_id(app_id)

            if existing_app:
                # Perform the update operation
                result = self.db_conn.db.apps.update_one({'_id': app_id}, {'$set': updated_app})
                if result.modified_count > 0:
                    return updated_app
                else:
                    return 'The app is already up-to-date'
            else:
                return None
        except Exception as e:
            # Log an error if the update fails
            self.logger.error(f'Error updating the app: {e}')
            return jsonify({'error': f'Error updating the app: {e}'}), 500

    def delete_app(self, app_id):
        try:
            # Check if the app exists before deleting
            existing_app = self.get_app_by_id(app_id)

            if existing_app:
                # Perform the delete operation
                self.db_conn.db.apps.delete_one({'_id': app_id})
                return existing_app
            else:
                return None
        except Exception as e:
            # Log an error if the deletion fails
            self.logger.error(f'Error deleting the app data: {e}')
            return jsonify({'error': f'Error deleting the app data: {e}'}), 500


if __name__ == '__main__':
    from models.app_models import AppModel

    logger = Logger()  # Create an instance of the logger
    db_conn = AppModel()  # Create an instance of the database model
    app_service = AppService(db_conn)  # Create an instance of the service class

    try:
        # Try to connect to the database
        db_conn.connect_to_database()

        # Example 
        # Add a new app
        # new_app = {
        #     'name': 'TestApp',
        #     'info': 'This is a test app',
        #     'description': 'An example description',
        #     'url': 'https://example.com',
        #     'logo_url': 'https://example.com/logo.png'
        # }
        # app_service.add_app(new_app)

        # Fetch all apps from the database
        apps = app_service.get_all_apps()
        if isinstance(apps, list):
            logger.info("Apps fetched successfully:")
            for app in apps:
                print(app)  # Print each app to the console
        else:
            print(apps)  # Print an error message if the retrieval fails

    except Exception as e:
        # Log any critical error that occurs
        logger.error(f'An error has occurred: {e}')
    finally:
        # Ensure the database connection is closed
        db_conn.close_connection()
        logger.info('Connection to database closed')
