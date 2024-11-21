from flask import Flask
from models.user_models import UserModel
from services.user_services import UserService
from routes.user_routes import UserRoutes

app = Flask(__name__)
db_conn = UserModel()
db_conn.connect_to_database
user_service = UserService(db_conn)
user_routes = UserRoutes(user_service)

if __name__ == 'main':
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()