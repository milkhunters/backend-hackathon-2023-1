from .user import UserRepo


class RepoFactory:
    def __init__(self, session, debug: bool = False):
        self._session = session
        self._debug = debug

    @property
    def user(self) -> UserRepo:
        return UserRepo(self._session)
