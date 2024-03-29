import logging
import os

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from src.models import tables
from src.db import create_psql_async_session
from src.middleware import JWTMiddlewareHTTP, JWTMiddlewareWS
from src.config import load_consul_config
from src.exceptions import APIError, handle_api_error, handle_404_error, handle_pydantic_error

from src.router import reg_root_api_router
from src.services.chat import ChatManager
from src.services.storage.s3 import S3Storage
from src.utils import RedisClient, AiohttpClient

config = load_consul_config(os.getenv('CONSUL_ROOT', "hackathon-2023-1-dev"), host="192.168.3.41")
logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO)

logging.debug("Инициализация приложения FastAPI.")
app = FastAPI(
    title=config.BASE.TITLE,
    debug=config.DEBUG,
    version=config.BASE.VERSION,
    description=config.BASE.DESCRIPTION,
    root_path="/api/v1" if not config.DEBUG else "",
    docs_url="/api/v1/docs" if config.DEBUG else "/docs",
    redoc_url="/api/v1/redoc" if config.DEBUG else "/redoc",
    contact={
        "name": config.BASE.CONTACT.NAME,
        "url": config.BASE.CONTACT.URL,
        "email": config.BASE.CONTACT.EMAIL,
    }
)


async def init_postgresql_db():
    engine, session = create_psql_async_session(
        username=config.DB.POSTGRESQL.USERNAME,
        password=config.DB.POSTGRESQL.PASSWORD,
        host=config.DB.POSTGRESQL.HOST,
        port=config.DB.POSTGRESQL.PORT,
        database=config.DB.POSTGRESQL.DATABASE,
        echo=config.DEBUG,
    )
    app.state.db_session = session

    async with engine.begin() as conn:
        # await conn.run_sync(tables.Base.metadata.drop_all)
        await conn.run_sync(tables.Base.metadata.create_all)


def init_s3_storage():
    app.state.file_storage = S3Storage(
        bucket=config.DB.S3.BUCKET,
        service_name=config.DB.S3.SERVICE_NAME,
        host=config.DB.S3.HOST,
        port=config.DB.S3.PORT,
        region_name=config.DB.S3.REGION,
        access_key=config.DB.S3.ACCESS_KEY,
        secret_access_key=config.DB.S3.SECRET_ACCESS_KEY,
    )


async def redis_pool(db: int = 0):
    return await redis.Redis(
        host=config.DB.REDIS.HOST,
        port=config.DB.REDIS.PORT,
        username=config.DB.REDIS.USERNAME,
        password=config.DB.REDIS.PASSWORD,
        db=db,
        encoding="utf-8",
        decode_responses=True,
    )


@app.on_event("startup")
async def on_startup():
    logging.debug("Executing FastAPI startup event handler.")
    await init_postgresql_db()
    init_s3_storage()

    app.state.redis = RedisClient(await redis_pool())
    app.state.http_client = AiohttpClient()
    app.state.chat_manager = ChatManager()

    logging.debug("FastAPI startup event handler executed.")


@app.on_event("shutdown")
async def on_shutdown():
    logging.debug("Executing FastAPI shutdown event handler.")
    # Gracefully close utilities.
    await app.state.redis.close()
    await app.state.http_client.close_session()


# custom OpenApi
def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema


app.openapi = custom_openapi
app.state.config = config

logging.debug("Adding routers.")
app.include_router(reg_root_api_router(config.DEBUG))
logging.debug("Registering exception handlers.")
app.add_exception_handler(APIError, handle_api_error)
app.add_exception_handler(404, handle_404_error)
app.add_exception_handler(RequestValidationError, handle_pydantic_error)
logging.debug("Registering middleware.")
app.add_middleware(JWTMiddlewareHTTP)
app.add_middleware(JWTMiddlewareWS)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
