"""Base class for services."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseService(ABC, Generic[T]):
    """Base class fror services."""

    @classmethod
    @abstractmethod
    async def create_instance(cls, *args: Any, **kwargs: Any) -> T:
        raise NotImplementedError
