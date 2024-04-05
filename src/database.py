"""Database module."""
import asyncio
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable
import logging

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from src.exceptions import DatabaseException

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    """비동기 데이터베이스 클래스"""

    def __init__(self, db_host:str):
        self._engine = create_async_engine(db_host)

        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                bind=self._engine,
            ),
            scopefunc=asyncio.current_task,
        )

    async def create_database(self) -> None:
        if self._engine.url.drivername != "sqlite+aiosqlite":
            raise ValueError("create_database should be used for test mode only.")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_database(self) -> None:
        if self._engine.url.drivername != "sqlite+aiosqlite":
            raise ValueError("drop_database should be used for test mode only.")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as e:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise DatabaseException("DB 처리 중 문제가 발생했습니다.", e)
        finally:
            await session.close()
            await self._session_factory.remove()

    async def connect(self):
        return await self._engine.connect()
