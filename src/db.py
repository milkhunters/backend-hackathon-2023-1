import urllib.parse
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base


def create_psql_async_session(
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        echo: bool = False,
) -> Tuple[AsyncEngine, sessionmaker]:
    engine = create_async_engine(
        "postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}".format(
            username=urllib.parse.quote_plus(username),
            password=urllib.parse.quote_plus(password),
            host=host,
            port=port,
            database=database
        ),
        echo=echo,
        future=True
    )
    return engine, sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()
