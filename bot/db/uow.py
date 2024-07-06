"""Unit of Work pattern implementation for managing transactions and repository instances.

Abstraction layer over SQLAlchemy sessions, facilitating transactional operations
across multiple repositories in a single unit of work.
"""

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db.repositories import _UserRepository


class _AbstractUnitOfWork(ABC):
    users: _UserRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWork(_AbstractUnitOfWork):
    """Unit of work implementation."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self.users = _UserRepository(self._session)
        return await super().__aenter__()

    async def commit(self) -> None:
        """Method to commit any changes made during the unit of work."""
        await self._session.commit()

    async def rollback(self) -> None:
        """If do not commit, or if exit the context manager by raising an error, do a rollback."""
        await self._session.rollback()
