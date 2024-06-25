from typing import Any, Self

from nc_py_api import AsyncNextcloud, FsNode

from bot.nextcloud.factory import FactorySubject


class BaseSearchService:
    def __init__(self, nc: AsyncNextcloud, fsnodes: list[FsNode]) -> None:
        self.nc = nc
        self.fsnodes = fsnodes


class SearchService(BaseSearchService, FactorySubject):
    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud, req: list[str], **kwargs: Any) -> Self:
        fsnodes = await nc.files.find(req, **kwargs)
        return cls(nc, fsnodes)
