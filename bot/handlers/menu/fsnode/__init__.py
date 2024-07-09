"""Router with fsnode menu messages."""

from aiogram import F, Router
from aiogram.types import ContentType
from aiogram_i18n import LazyFilter

from .back import back
from .cancel import cancel_callback, cancel_message
from .delete import delete, delete_confirm
from .download import download
from .menu import menu
from .new import (
    incorrectly_mkdir,
    mkdir,
    mkdir_start,
    new,
    upload,
    upload_incorrectly,
    upload_start,
)
from .pag import pag
from .select import select
from bot.filters import AuthorizedFilter, OnlyPrivateFilter
from bot.keyboards.callback_data_factories import FsNodeData, FsNodeMenuActions, FsNodeMenuData
from bot.states import FsNodeMenuStatesGroup


def fsnode_menu_router() -> Router:
    """Build router with fsnode menu messages.

    :return: Router with fsnode menu messages.
    """
    router = Router()

    # Menu block.
    router.message.register(
        menu,
        LazyFilter("fsnode-menu-button"),
        AuthorizedFilter(),
        OnlyPrivateFilter(),
    )

    # Cancel block.
    router.callback_query.register(
        cancel_callback,
        FsNodeMenuData.filter(F.action == FsNodeMenuActions.CANCEL),
    )
    router.message.register(
        cancel_message,
        FsNodeMenuStatesGroup.UPLOAD,
        LazyFilter("stop-button"),
    )
    router.message.register(
        cancel_message,
        FsNodeMenuStatesGroup.MKDIR,
        LazyFilter("cancel-button"),
    )

    # New fsnode block.
    router.callback_query.register(new, FsNodeMenuData.filter(F.action == FsNodeMenuActions.NEW))

    router.callback_query.register(
        upload_start,
        FsNodeMenuData.filter(F.action == FsNodeMenuActions.UPLOAD),
    )
    router.message.register(
        upload,
        FsNodeMenuStatesGroup.UPLOAD,
        F.content_type.in_({ContentType.DOCUMENT}),
    )
    router.message.register(upload_incorrectly, FsNodeMenuStatesGroup.UPLOAD)

    router.callback_query.register(
        mkdir_start,
        FsNodeMenuData.filter(F.action == FsNodeMenuActions.MKDIR),
    )
    router.message.register(
        mkdir,
        FsNodeMenuStatesGroup.MKDIR,
        F.text.regexp(r"^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]?$"),
    )
    router.message.register(incorrectly_mkdir, FsNodeMenuStatesGroup.MKDIR)

    # Pagination block.
    router.callback_query.register(
        pag,
        FsNodeMenuData.filter(
            F.action.in_({FsNodeMenuActions.PAG_BACK, FsNodeMenuActions.PAG_NEXT}),
        ),
    )

    # Delete block.
    router.callback_query.register(
        delete,
        FsNodeMenuData.filter(F.action == FsNodeMenuActions.DELETE),
    )
    router.callback_query.register(
        delete_confirm,
        FsNodeMenuData.filter(F.action == FsNodeMenuActions.DELETE_CONFIRM),
    )

    # Download block.
    router.callback_query.register(
        download,
        FsNodeMenuData.filter(F.action == FsNodeMenuActions.DOWNLOAD),
    )

    # Back block.
    router.callback_query.register(back, FsNodeMenuData.filter(F.action == FsNodeMenuActions.BACK))

    # Select.
    router.callback_query.register(select, FsNodeData.filter())

    return router
