import typing
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.websockets import WebSocket

from src.models.enums import ErrorType
from src.models.schemas import Error, FieldErrorItem
from src.views import BaseView


class APIError(StarletteHTTPException):
    def __init__(
            self,
            message: str = "Error",
            status_code: int = 400,
            headers: typing.Optional[dict] = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(status_code=status_code, headers=headers)


class BadRequest(APIError):
    status_code = 400
    message = "Bad request"

    def __init__(self, message: str = None) -> None:
        super().__init__(message=message if message else self.message, status_code=self.status_code)


class AccessDenied(APIError):
    status_code = 403
    message = "Access denied"

    def __init__(self, message: str = None) -> None:
        super().__init__(message=message if message else self.message, status_code=self.status_code)


class NotFound(APIError):
    status_code = 404
    message = "Not Found"

    def __init__(self, message: str = None) -> None:
        super().__init__(message=message if message else self.message, status_code=self.status_code)


class AlreadyExists(APIError):
    status_code = 409
    message = "Already exists"

    def __init__(self, message: str = None) -> None:
        super().__init__(message=message if message else self.message, status_code=self.status_code)


async def handle_api_error(request, exc):
    if isinstance(request, WebSocket):
        await request.accept()
        await request.close(code=int(f'{exc.status_code}0'), reason=exc.message)
        return
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content=BaseView(
                error=Error(
                    type=ErrorType.MESSAGE,
                    content=exc.message
                )
            ).dict()
        )


async def handle_pydantic_error(request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=BaseView(
            error=Error(
                type=ErrorType.FIELD_LIST,
                content=[
                    FieldErrorItem(
                        field=field.get('loc', ['none'])[-1],
                        location=field.get('loc', []),
                        message=field.get('msg', 'No message'),
                        type=field.get('type', 'empty')
                    ) for field in exc.errors()
                ]
            )
        ).dict()
    )


async def handle_404_error(request, exc):
    if isinstance(request, WebSocket):
        await request.accept()
        await request.close(code=int(f'{exc.status_code}0'), reason=exc.message)
        return
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content=BaseView(
                error=Error(
                    type=ErrorType.MESSAGE,
                    content='Not Found'
                )
            ).dict()
        )
