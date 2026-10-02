from app.models.user import User


class UserRepo():

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._next_id = 1

    def get_by_username(self, username: str) -> User | None:
        return self._users.get(username)

    def create(self, username: str, email: str, hashed_password: str,
                    roles: list[str]) -> User:
        user = User(id=self._next_id, username=username, email=email, hashed_password=hashed_password, roles=roles)
        self._users[username] = user
        self._next_id += 1
        return user


user_repo = UserRepo()


