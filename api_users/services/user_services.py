from flask import jsonify
from logger.logger_users import Logger

class UserService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn
    
    def get_all_users(self):
        try:
            users = list(self.db_conn.db.users.find())
            return users
        except Exception as e:
            self.logger.error(f'Error fetching all users from the database: {e}')
            return jsonify({'error': 'Failed to fetch users'}), 500

if __name__ == '__main__':
    from models.user_models import UserModel
    logger = Logger()
    db_conn = UserModel()
    user_service = UserService(db_conn)
    try:
        db_conn.connect_to_database()
        users = users_service.get_all_users()
        logger.info(f'Users fetched: {users}')
    except Exception as e:
        logger.error(f'Error fetching all users: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database closed')