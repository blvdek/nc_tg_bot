"""Module providing services for interacting with the Nextcloud API."""

from .fsnode import FsNodeService, PrevFsNodeService, RootFsNodeService
from .search import SearchService
from .trashbin import TrashbinService

__all__ = (
    "RootFsNodeService",
    "FsNodeService",
    "PrevFsNodeService",
    "TrashbinService",
    "SearchService",
)
