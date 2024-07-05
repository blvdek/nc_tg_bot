"""Service that provide methods for fsnode searching in Nextcoud."""

from typing import Any, Self

from nc_py_api import AsyncNextcloud, FsNode

from bot.nextcloud.factory import FactorySubject


class BaseSearchService:
    """Base class for Nextcloud search service.

    :param nc: The Nextcloud client object.
    :param fsnodes: The list of Nextcloud file nodes.
    """

    def __init__(self, nc: AsyncNextcloud, fsnodes: list[FsNode]) -> None:
        self.nc = nc
        self.fsnodes = fsnodes


class SearchService(FactorySubject[BaseSearchService], BaseSearchService):
    """Implementation of Nextcloud search service."""

    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud, req: list[str], **kwargs: Any) -> Self:
        """Create a Nextcloud search service instance.

        :param nc: The Nextcloud client object.
        :param req: The list of search parameters.
        :param kwargs: Additional search parameters.
        :return: The Nextcloud search service instance.
        """
        fsnodes = await nc.files.find(req, **kwargs)
        return cls(nc, fsnodes)
