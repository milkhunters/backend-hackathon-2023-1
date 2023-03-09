import asyncio

import pytest
from fastapi.testclient import TestClient

from src.dependencies.repos import get_repos
from src.services.repository import RepoFactory
from src.db import create_sqlite_async_session
from src.app import app, tables, redis_pool
from src.utils import RedisClient


async def get_repos_fake():
    async with app.state.db_session() as session:
        yield RepoFactory(session, debug=True)


app.dependency_overrides[get_repos] = get_repos_fake


async def on_startup_event():
    """
            for testing use 'test.db'
        """
    engine, session = create_sqlite_async_session(
        database='test.db',
        echo=False,
    )

    app.state.db_session = session
    app.state.db_engine = engine

    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.drop_all)
        await conn.run_sync(tables.Base.metadata.create_all)

    app.state.redis = RedisClient(await redis_pool(1))


app.on_event("startup")(on_startup_event)

client = TestClient(app)
