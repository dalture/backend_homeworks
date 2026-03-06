from schemas import BaseUser

users = []

class UserService:
    def __init__(self):
        self.user_mock_db = users

    def get_all_users(self):
        return [BaseUser(**user.model_dump()) for user in self.user_mock_db]