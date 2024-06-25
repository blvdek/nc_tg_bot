from abc import ABC, abstractmethod
from typing import Any, TypeVar

from bot.nextcloud.exceptions import ClassNotFoundError

T = TypeVar("T")


class FactorySubject(ABC):
    @classmethod
    @abstractmethod
    async def create_instance(cls, *args: Any, **kwargs: Any) -> T:
        raise NotImplementedError


class NCSrvFactory:
    @staticmethod
    def get(class_name: str) -> type[FactorySubject]:
        raw_subclasses_ = FactorySubject.__subclasses__()
        classes = {c.__name__: c for c in raw_subclasses_}
        class_ = classes.get(class_name, None)
        if class_ is not None:
            return class_

        raise ClassNotFoundError
