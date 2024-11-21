from flask import Blueprint, jsonify

class UserRoutes(Blueprint):
    def __init__(self,user_service):
        super().__init__('user_routes', __name__)
        self.user_service = user_service
        self.register_routes()
    
    def register_routes(self):
        self.route('/api/v1/users', methods=['GET'])(self.get_users)
    
    def get_users():
        users = self.user_service.get_all_users()
        return jsonify(users), 200