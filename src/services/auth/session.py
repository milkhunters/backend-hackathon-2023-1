import uuid
from typing import Optional

from fastapi import Request, Response
from starlette.websockets import WebSocket

from src.utils import RedisClient


class SessionManager:
    COOKIE_EXP = 31536000
    REDIS_EXP = 2592000
    COOKIE_PATH = "/api"
    COOKIE_DOMAIN = None
    COOKIE_SESSION_KEY = "session_id"

    def __init__(self, redis_client: RedisClient, config, debug: bool = False):
        self._redis_client = redis_client
        self._config = config
        self._debug = debug

    def get_session_id(self, req_obj: Request | WebSocket) -> Optional[int]:
        """
        Получить идентификатор сессии из куков

        :param req_obj:
        :return: session_id
        """

        str_cookie_session_id = req_obj.cookies.get(self.COOKIE_SESSION_KEY)
        try:
            cookie_session_id = int(str_cookie_session_id)
        except (ValueError, TypeError):
            return None
        return cookie_session_id

    async def set_session_id(
            self,
            response: Response,
            refresh_token: str,
            session_id: int = None
    ) -> int:
        """
        Генерирует (если не передано) и устанавливает сессию в redis и в куки

        :param response: 
        :param refresh_token: 
        :param session_id: 
        :return: session_id
        """
        if not session_id:
            session_id = uuid.uuid4().int
        response.set_cookie(
            key=self.COOKIE_SESSION_KEY,
            value=str(session_id),
            secure=self._config.IS_SECURE_COOKIE,
            httponly=True,
            samesite="none",
            max_age=self.COOKIE_EXP,
            path=self.COOKIE_PATH
        )
        await self._redis_client.set(str(session_id), refresh_token, expire=self.REDIS_EXP)
        return session_id

    async def delete_session_id(self, session_id: int, response: Response) -> None:
        """
        Удаляет сессию из куков и из redis

        :param session_id
        :param response
        """
        await self._redis_client.delete(str(session_id))
        response.delete_cookie(
            key=self.COOKIE_SESSION_KEY,
            secure=self._config.IS_SECURE_COOKIE,
            httponly=True,
            samesite="none",
            path=self.COOKIE_PATH
        )

    async def is_valid_session(self, session_id: int | str, cookie_refresh_token: str) -> bool:
        """
        Проверяет валидность сессии
        :param session_id:
        :param cookie_refresh_token:
        :return: True or False
        """
        refresh_token_from_redis = await self._redis_client.get(str(session_id))
        if not refresh_token_from_redis:
            return False
        if refresh_token_from_redis != cookie_refresh_token:
            return False
        return True
