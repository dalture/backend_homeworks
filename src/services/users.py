from schemas import BaseUser

users = [
    BaseUser(
        id=1,
        name="Darina",
        surname="Ivanova",
        email="darina.ivanova@gmail.com"
    ),
    BaseUser(
        id=2,
        name="Maxim",
        surname="Petrov",
        email="max.petrov@gmail.com"
    ),
    BaseUser(
        id=3,
        name="Anna",
        surname="Smirnova",
        email="anna.smirnova@gmail.com"
    ),
    BaseUser(
        id=4,
        name="Ivan",
        surname="Kuznetsov",
        email="ivan.kuznetsov@gmail.com"
    ),
    BaseUser(
        id=5,
        name="Elena",
        surname="Sokolova",
        email="elena.sokolova@gmail.com"
    ),
    BaseUser(
        id=6,
        name="Dmitry",
        surname="Volkov",
        email="d.volkov@gmail.com"
    ),
]


class UserService:
    def __init__(self):
        self.user_mock_db = users

    def get_all_users(self):
        return [BaseUser(**user.model_dump()) for user in self.user_mock_db]