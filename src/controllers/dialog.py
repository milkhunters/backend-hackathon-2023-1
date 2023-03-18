import uuid

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi import status as http_status
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory
from src.views import dialog
from src.views.dialog import DialogListResponse, DialogResponse

router = APIRouter()


@router.get("/list", response_model=DialogListResponse, status_code=http_status.HTTP_200_OK)
async def get_dialog_list(services: ServiceFactory = Depends(get_services)):
    return DialogListResponse(message=await services.chat.get_my_dialogs())


@router.get("/open", response_model=DialogResponse, status_code=http_status.HTTP_200_OK)
async def open_dialog(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return DialogResponse(message=await services.chat.get_dialog_by_user(user_id))


@router.websocket("/{dialog_id}/ws")
async def open_dialog(dialog_id: uuid.UUID, websocket: WebSocket, services: ServiceFactory = Depends(get_services)):
    await services.chat.subscribe_to_chat(websocket, dialog_id)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <button onclick="connect()">Connect to WS</button>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            let ws;
            function connect(){
                ws = new WebSocket("ws://127.0.0.1:8000/api/v1/dialog/0b039a23-8fd3-404a-897b-59b5215baf96/ws");
                ws.onmessage = async function(event) {
                    const messages = document.getElementById('messages')
                    const message = document.createElement('li')

                    const str_data = await event.data.text()
                    const json_data = JSON.parse(str_data)

                    const content = document.createTextNode(str_data);
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                ws.onclose = function (event) {
                    console.log('Socket is closed.', event.reason, event.code);
                    alert(event.code + ' ' + event.reason);
                };
            }


            function sendMessage(event) {
                const input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/test", status_code=http_status.HTTP_200_OK)
async def test(request: Request):
    return HTMLResponse(html)