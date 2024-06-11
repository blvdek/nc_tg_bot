import io
import pathlib
from abc import ABC
from typing import Any

from aiogram.types import BufferedInputFile
from nc_py_api import AsyncNextcloud, FsNode
from typing_extensions import Self

from bot.core import settings


# TODO: cls, static, default method or funtion.
async def _check_is_root_id(nc: AsyncNextcloud, file_id: str) -> FsNode | None:
    """Nextcloud does not return the root file by id."""
    root_files = await nc.files.listdir(exclude_self=False)
    if root_files[0].file_id == file_id:
        return root_files[0]
    return None


class _AbstractFleManager(ABC):
    def __init__(self, nc: AsyncNextcloud, file: FsNode) -> None:
        self._nc = nc
        self.file = file

    # TODO: Think about name and logick.
    @classmethod
    async def create_instance_by_id(cls, nc: AsyncNextcloud, file_id: str) -> Self | None:
        file = await nc.files.by_id(file_id)
        if file is None:
            root_file = await _check_is_root_id(nc, file_id)
            return None if root_file is None else cls(nc, root_file)
        return cls(nc, file)

    # TODO: Think about name and logick.
    @classmethod
    async def create_prev_instance_by_id(cls, nc: AsyncNextcloud, file_id: str) -> Self | None:
        file = await nc.files.by_id(file_id)
        if file is None:
            root_file = await _check_is_root_id(nc, file_id)
            return None if root_file is None else cls(nc, root_file)

        path = pathlib.Path(file.user_path)
        prev_path = str(path.parent) if str(path.parent) != "." else ""

        prev_file = await nc.files.by_path(prev_path)
        if prev_file is None:
            return None
        return cls(nc, prev_file)

    # TODO: Think about name.
    @classmethod
    async def create_root_instance(cls, nc: AsyncNextcloud) -> Self:
        root_file = await nc.files.by_path("")
        return cls(nc, root_file)


class FileManager(_AbstractFleManager):
    def __init__(self, nc: AsyncNextcloud, file: FsNode) -> None:
        self._nc = nc
        self.file = file

    def _update_name(self, name: str, files: list[FsNode]) -> str:
        i = 1
        path = pathlib.Path(name)
        while name in [file.name for file in files]:
            name = f"{path.stem} ({i}){path.suffix}"
            i += 1
        return name

    async def listdir(self, **kwargs: Any) -> list[FsNode]:
        files: list[FsNode] = await self._nc.files.listdir(self.file, **kwargs)
        return files

    async def mkdir(self, name: str) -> FsNode:
        if not self.file.is_dir:
            msg = "..."
            raise RuntimeError(msg)
        name = self._update_name(name, await self.listdir(depth=1, exclude_self=True))
        await self._nc.files.mkdir(f"{self.file.user_path}{name}")

    async def delete(self) -> None:
        await self._nc.files.delete(self.file)

    async def download(self) -> BufferedInputFile:
        buff = io.BytesIO()
        await self._nc.files.download2stream(self.file, buff, chunk_size=settings.nextcloud.chunk_size)

        buff.seek(0)
        return BufferedInputFile(buff.read(), filename=self.file.name)

    async def upload(self, buff: io.BytesIO, name: str) -> None:
        name = self._update_name(name, await self.listdir(depth=1, exclude_self=True))

        buff.seek(0)
        await self._nc.files.upload_stream(
            f"{self.file.user_path}{name}",
            buff,
            chunk_size=settings.nextcloud.chunk_size,
        )

    async def direct_download(self) -> str:
        res: dict[str, str] = await self._nc.ocs(
            "POST",
            "/ocs/v2.php/apps/dav/api/v1/direct",
            params={"fileId": self.file.file_id},
        )
        return res["url"]
