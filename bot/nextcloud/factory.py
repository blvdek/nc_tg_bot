"""Factory class for creating instances of specific classes."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from bot.nextcloud.exceptions import ClassNotFoundError

T = TypeVar("T")


class FactorySubject(ABC, Generic[T]):
    """Abstract base class for classes that can be instantiated using the factory.

    This class serves as an abstract base class for classes that can be instantiated using the factory.
    """

    @classmethod
    @abstractmethod
    async def create_instance(cls, *args: Any, **kwargs: Any) -> T:
        """Method, which should be implemented by subclasses. It should create an instance of the class."""
        raise NotImplementedError


class NCSrvFactory:
    """Factory for retrieving classes based on their name.

    :param class_name: The name of the class to retrieve.
    """

    @staticmethod
    def get(class_name: str) -> type[FactorySubject[Any]]:
        """Retrieves a class based on its name."""
        raw_subclasses_ = FactorySubject.__subclasses__()
        classes = {c.__name__: c for c in raw_subclasses_}
        class_ = classes.get(class_name)
        if class_ is not None:
            return class_

        raise ClassNotFoundError
