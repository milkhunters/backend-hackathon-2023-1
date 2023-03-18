import uuid
from typing import Optional, AsyncGenerator, Any

from fastapi.websockets import WebSocket

from src.models import schemas
from src.services.chat.wsmanager import WSJWTConnectionManager


class ChatManager:
    def __init__(self):
        self._rooms: dict = {}

    async def connect(self, websocket: WebSocket, room_id: uuid.UUID) -> None:
        assert room_id in self._rooms
        await self._rooms[room_id]['ws'].connect(websocket)

    async def disconnect(self, websocket: WebSocket, room_id: int) -> None:
        ws: WSJWTConnectionManager = await self._rooms[room_id]['ws']
        await ws.disconnect(websocket)
        if ws.connections == 0:
            self._rooms.pop(room_id)


    async def create_room(self, room_id) -> None:
        assert room_id not in self._rooms

        self._rooms[room_id] = dict(
            ws=WSJWTConnectionManager()
        )

    def is_exists(self, room_id: uuid.UUID) -> bool:
        return room_id in self._rooms

    async def send_data(self, room_id: uuid.UUID, data: dict):
        ws: WSJWTConnectionManager = self._rooms[room_id]['ws']
        await ws.broadcast(data)

    def get_room_ws(self, room_id: uuid.UUID) -> WSJWTConnectionManager:
        return self._rooms[room_id]['ws']

    async def close(self, room_id) -> None:
        assert room_id in self._rooms

        await self._rooms[room_id]['ws'].close(
            code=1000,
            reason='Terminal closed'
        )
        self._rooms.pop(room_id)
