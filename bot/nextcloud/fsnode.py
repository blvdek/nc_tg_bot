import io
import pathlib
from typing import Self

from aiogram.types import BufferedInputFile
from nc_py_api import AsyncNextcloud, FsNode

from bot.core import settings
from bot.nextcloud.exceptions import FsNodeNotFoundError
from bot.nextcloud.factory import FactorySubject, T


class BaseFsNodeService:
    def __init__(self, nc: AsyncNextcloud, fsnode: FsNode, attached_fsnodes: list[FsNode]) -> None:
        self.nc = nc
        self.fsnode = fsnode
        self.attached_fsnodes = attached_fsnodes

    @staticmethod
    async def _check_is_root_id(nc: AsyncNextcloud, file_id: str) -> FsNode:
        fsnodes_list = await nc.files.listdir(exclude_self=False)
        if fsnodes_list[0].file_id == file_id:
            return fsnodes_list[0], fsnodes_list[1:]
        raise FsNodeNotFoundError

    def _generate_unique_name(self, name: str) -> str:
        i = 1
        path = pathlib.Path(name)
        while name in [fsnode.name for fsnode in self.attached_fsnodes]:
            name = f"{path.stem} ({i}){path.suffix}"
            i += 1
        return name

    async def mkdir(self, name: str) -> FsNode:
        if not self.fsnode.is_dir:
            msg = "..."
            raise RuntimeError(msg)

        name = self._generate_unique_name(name)
        new_dir = await self.nc.files.mkdir(f"{self.fsnode.user_path}{name}")

        self.attached_fsnodes.append(new_dir)

    async def delete(self) -> None:
        await self.nc.files.delete(self.fsnode)

    async def download(self) -> BufferedInputFile:
        buff = io.BytesIO()
        await self.nc.files.download2stream(self.fsnode, buff, chunk_size=settings.nextcloud.chunk_size)

        buff.seek(0)
        return BufferedInputFile(buff.read(), filename=self.fsnode.name)

    async def upload(self, buff: io.BytesIO, name: str) -> None:
        if not self.fsnode.is_dir:
            msg = "..."
            raise RuntimeError(msg)

        name = self._generate_unique_name(name)

        buff.seek(0)
        await self.nc.files.upload_stream(
            f"{self.fsnode.user_path}{name}",
            buff,
            chunk_size=settings.nextcloud.chunk_size,
        )

    async def direct_download(self) -> str:
        res: dict[str, str] = await self.nc.ocs(
            "POST",
            "/ocs/v2.php/apps/dav/api/v1/direct",
            params={"fileId": self.fsnode.file_id},
        )
        return res["url"]


class RootFsNodeService(FactorySubject[BaseFsNodeService], BaseFsNodeService):
    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud) -> Self:
        fsnodes_list = await nc.files.listdir(exclude_self=False)
        return cls(nc, fsnodes_list[0], fsnodes_list[1:])


class FsNodeService(FactorySubject[BaseFsNodeService], BaseFsNodeService):
    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud, file_id: str) -> Self:
        fsnode = await nc.files.by_id(file_id)
        if fsnode is None:
            fsnode, attached_fsnodes = await cls._check_is_root_id(nc, file_id)
            return cls(nc, fsnode, attached_fsnodes)
        attached_fsnodes = await nc.files.listdir(fsnode)
        return cls(nc, fsnode, attached_fsnodes)


class PrevFsNodeService(FactorySubject[BaseFsNodeService], BaseFsNodeService):
    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud, file_id: str) -> Self:
        fsnode = await nc.files.by_id(file_id)
        if fsnode is None:
            fsnode, attached_fsnodes = await cls._check_is_root_id(nc, file_id)
            return cls(nc, fsnode, attached_fsnodes)

        path = pathlib.Path(fsnode.user_path)
        prev_path = str(path.parent) if str(path.parent) != "." else ""

        fsnode = await nc.files.by_path(prev_path)
        attached_fsnodes = await nc.files.listdir(fsnode)
        return cls(nc, fsnode, attached_fsnodes)
