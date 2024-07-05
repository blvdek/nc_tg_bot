from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Base

T = TypeVar("T", bound=Base)


class _AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, record_id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, **filters: Any) -> Sequence[Base]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, record: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, record: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, record_id: int) -> None:
        raise NotImplementedError


class _Repository(_AbstractRepository[T], ABC):
    type_model: type[T]
    session: AsyncSession

    def __init__(self, session: AsyncSession, model_cls: type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    async def get_by_id(self, ident: int) -> T | None:
        return await self._session.get(self._model_cls, ident)

    async def get_many(self, limit: int = 100, order_by: Any = None, **filters: Any) -> Sequence[Base]:
        statement = select(self._model_cls).where(**filters).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)
        return (await self._session.scalars(statement)).all()

    async def add(self, record: T) -> T:
        await self._session.merge(record)
        await self._session.flush()
        return record

    async def update(self, record: T) -> T:
        return await self.add(record)

    async def delete(self, ident: int) -> None:
        record = await self.get_by_id(ident)
        if record is not None:
            await self._session.delete(record)
            await self._session.flush()
