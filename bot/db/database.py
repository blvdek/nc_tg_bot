"""Creates an asynchronous SQLAlchemy engine and session maker."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core import settings

_engine = create_async_engine(settings.db.url, pool_pre_ping=True)
session_maker = async_sessionmaker(_engine)
