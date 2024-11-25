from flask import Flask
from models.app_models import AppModel  # Import the database model
from services.app_services import AppService  # Import the app service
from schemas.app_schemas import AppSchema  # Import the schema for validation
from routes.app_routes import AppRoutes  # Import the API routes
from flasgger import Swagger  # Import Swagger for API documentation
from flask_cors import CORS  # Import CORS for cross-origin requests

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for the application

# Initialize Swagger for API documentation
swagger = Swagger(app)

# Create the database connection
db_conn = AppModel()
db_conn.connect_to_database()  # Connect to the MongoDB database

# Initialize the service and schema for handling app logic and validation
app_service = AppService(db_conn)
app_schema = AppSchema()

# Create and register the app routes
app_routes = AppRoutes(app_service, app_schema)
app.register_blueprint(app_routes)

# Entry point for running the Flask application
if __name__ == '__main__':
    try:
        app.run(debug=True)  # Run the app in debug mode for development
    finally:
        db_conn.close_connection()  # Ensure the database connection is closed properly
