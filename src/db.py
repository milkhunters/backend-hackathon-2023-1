import urllib.parse
from typing import Tuple

from sqlalchemy import TypeDecorator, Integer
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


def create_sqlite_async_session(database: str, echo: bool = False) -> Tuple[AsyncEngine, sessionmaker]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///{database}".format(
            database=database
        ),
        echo=echo,
        future=True
    )
    return engine, sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()


class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enums and storing the enums's *value* in the db.
    The default would have stored the enums's *name* (ie the string).
    """
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)
