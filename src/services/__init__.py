from src.models import tables
from . import repository
from . import auth
from .banner import BannerApplicationService
from .chat import ChatApplicationService
from .file import FileApplicationService
from .user import UserApplicationService
from .article import ArticleApplicationService


class ServiceFactory:
    def __init__(
            self,
            repo_factory: repository.RepoFactory,
            *,
            current_user: tables.User,
            config, redis_client,
            chat_manager,
            file_storage,
            debug: bool = True
    ):
        self._repo = repo_factory
        self._current_user = current_user
        self._config = config
        self._redis_client = redis_client
        self._chat_manager = chat_manager
        self._file_storage = file_storage
        self._debug = debug

    @property
    def user(self) -> UserApplicationService:
        return UserApplicationService(self._repo.user, file_repo=self._repo.file, current_user=self._current_user)

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
    def chat(self) -> ChatApplicationService:
        return ChatApplicationService(
            chat_repo=self._repo.chat,
            user_chat_repo=self._repo.user_chat,
            user_repo=self._repo.user,
            chat_manager=self._chat_manager,
            current_user=self._current_user,
            message_repo=self._repo.message
        )

    @property
    def file(self) -> FileApplicationService:
        return FileApplicationService(
            file_repo=self._repo.file,
            file_storage=self._file_storage,
            current_user=self._current_user
        )

    @property
    def article(self) -> ArticleApplicationService:
        return ArticleApplicationService(self._repo.article, current_user=self._current_user)

    @property
    def banner(self) -> BannerApplicationService:
        return BannerApplicationService(banner_repo=self._repo.banner, current_user=self._current_user)
