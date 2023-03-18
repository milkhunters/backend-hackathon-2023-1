from .chat import ChatRepo
from .file import FileRepo
from .message import MessageRepo
from .user import UserRepo

from .user_chat import UserChatAssociationRepo
from .article import ArticleRepo


class RepoFactory:
    def __init__(self, session, debug: bool = False):
        self._session = session
        self._debug = debug

    @property
    def user(self) -> UserRepo:
        return UserRepo(self._session)

    @property
    def chat(self) -> ChatRepo:
        return ChatRepo(self._session)

    @property
    def user_chat(self) -> UserChatAssociationRepo:
        return UserChatAssociationRepo(self._session)

    @property
    def message(self):
        return MessageRepo(self._session)

    @property
    def file(self) -> FileRepo:
        return FileRepo(self._session)

    @property
    def article(self) -> ArticleRepo:
        return ArticleRepo(self._session)
