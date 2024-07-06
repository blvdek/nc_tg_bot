"""Service that provide methods for managing the trash bin in the Nextcloud."""

from typing import Self

from nc_py_api import AsyncNextcloud, FsNode

from bot.nextcloud._base import BaseService


class BaseTrashbinService:
    """Base class for managing the trash bin in the Nextcloud.

    :param nc: The Nextcloud client object.
    :param trashbin: List of files in the trash bin.
    """

    def __init__(self, nc: AsyncNextcloud, trashbin: list[FsNode]) -> None:
        self.nc = nc
        self.trashbin = trashbin

    def _get_trashbin_item_by_id(self, file_id: str) -> FsNode | None:
        """Get an item from the trash bin by its ID.

        :param file_id: The file id of the fsnode.
        :return: Item from the trash bin or None if not found.
        """
        for trashbin_item in self.trashbin:
            if trashbin_item.file_id == file_id:
                return trashbin_item
        return None

    async def delete(self, file_id: str) -> None:
        """Delete an item from the trash bin by its ID.

        :param file_id: The file id of the fsnode.
        """
        trashbin_item = self._get_trashbin_item_by_id(file_id)
        if trashbin_item is None:
            msg = "The file ID not found in the trashbin."
            raise ValueError(msg)

        await self.nc.files.trashbin_delete(trashbin_item)
        self.trashbin.remove(trashbin_item)

    async def restore(self, file_id: str) -> None:
        """Restore an item from the trash bin by its ID.

        :param file_id: The file id of the fsnode.
        """
        trashbin_item = self._get_trashbin_item_by_id(file_id)
        if trashbin_item is None:
            msg = "The file ID not found in the trashbin."
            raise ValueError(msg)

        await self.nc.files.trashbin_restore(trashbin_item)
        self.trashbin.remove(trashbin_item)

    async def cleanup(self) -> None:
        """Clean up the trash bin by deleting all items."""
        await self.nc.files.trashbin_cleanup()
        self.trashbin = []

    def get_size(self) -> int:
        """Calculate the total size of files in the trash bin.

        :return: Total size of files in the trash bin.
        """
        size = 0
        for fsnode in self.trashbin:
            size += fsnode.info.size
        return size


class TrashbinService(BaseService[BaseTrashbinService], BaseTrashbinService):
    """Implementation of the Trashbin service."""

    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud) -> Self:
        """Create an instance of the trashbin service.

        :param nc: The Nextcloud client object.
        :return: Instance of the TrashbinService.
        """
        trashbin = await nc.files.trashbin_list()
        return cls(nc, trashbin)
