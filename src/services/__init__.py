from src.models import tables
from . import repository
from . import auth
from .admin import AdminApplicationService
from .chat import ChatApplicationService
from .user import UserApplicationService


class ServiceFactory:
    def __init__(
            self,
            repo_factory: repository.RepoFactory,
            *,
            current_user: tables.User,
            config, redis_client,
            chat_manager,
            debug: bool = False
    ):
        self._repo = repo_factory
        self._current_user = current_user
        self._config = config
        self._redis_client = redis_client
        self._chat_manager = chat_manager
        self._debug = debug

    @property
    def user(self) -> UserApplicationService:
        return UserApplicationService(self._repo.user, current_user=self._current_user, debug=self._debug)

    @property
    def auth(self) -> auth.AuthApplicationService:
        return auth.AuthApplicationService(
            jwt=auth.JWTManager(config=self._config, debug=self._debug),
            session=auth.SessionManager(redis_client=self._redis_client, config=self._config, debug=self._debug),
            user_repo=self._repo.user,
            current_user=self._current_user,
            debug=self._debug
        )

    @property
    def admin(self) -> AdminApplicationService:
        return AdminApplicationService(self._repo.user, current_user=self._current_user, debug=self._debug)

    @property
    def chat(self) -> ChatApplicationService:
        return ChatApplicationService(
            chat_repo=self._repo.chat,
            user_chat_repo=self._repo.user_chat,
            user_repo=self._repo.user,
            chat_manager=self._chat_manager,
            current_user=self._current_user
        )
