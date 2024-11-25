import os
from logger.logger_apps import Logger
from pymongo import MongoClient

class AppModel:  # Define the class to manage the database connection
    def __init__(self):  # Initialize the class
        self.client = None  # MongoDB client will be stored here
        self.db = None  # Database object will be stored here
        self.logger = Logger()  # Create a logger instance

    def connect_to_database(self):
        # Get MongoDB credentials from environment variables
        mongodb_user = os.environ.get('MONGODB_USER')
        mongodb_pass = os.environ.get('MONGODB_PASS')
        mongodb_host = os.environ.get('MONGODB_HOST')

        # Check if the required environment variables are set
        if not mongodb_user or not mongodb_pass or not mongodb_host:
            self.logger.critical('MongoDB environment variables are required but missing')
            raise ValueError('Set environment variables: MONGODB_USER, MONGODB_PASS, MONGODB_HOST')

        try:
            # Connect to the MongoDB database
            self.client = MongoClient(
                host=mongodb_host,  # Database host
                port=27017,  # Default MongoDB port
                username=mongodb_user,  # Database username
                password=mongodb_pass,  # Database password
                authSource='admin',  # Authentication database
                authMechanism='SCRAM-SHA-256',  # Authentication method
                serverSelectionTimeoutMS=5000  # Timeout for server selection
            )
            self.db = self.client['microservices']  # Access the "microservices" database
            # Log a message if the connection is successful
            if self.db.list_collection_names():  
                self.logger.info('Connected to MongoDB database successfully')

        except Exception as e:
            # Log a critical error message if the connection fails
            self.logger.critical(f'Failed to connect to the database: {e}')
            raise

    def close_connection(self):
        # Close the connection to the database if it is open
        if self.client:
            self.client.close()

if __name__ == '__main__':
    db_conn = AppModel()  # Create an instance of the AppModel class

    try: 
        # Try to connect to the database
        db_conn.connect_to_database()
    except Exception as e:
        # Log any errors that occur during the connection
        db_conn.logger.critical(f'An error occurred: {e}')
    finally: 
        # Ensure the database connection is closed
        db_conn.close_connection()
        db_conn.logger.info('Connection to the database was successfully closed')
