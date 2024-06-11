from aiogram import F, Router
from aiogram.types import ContentType

from .back import back
from .cancel import cancel_callback, cancel_message
from .delete import delete, delete_confirm
from .download import download
from .menu import menu
from .mkdir import incorrectly_mkdir, mkdir, start_mkdir
from .pag import pag
from .select import select
from .upload import upload, upload_incorrectly, upload_start
from bot.filters import AuthorizedFilter, LocalizedTextFilter, MsgAuthorFilter
from bot.keyboards import callback_data_factories as cdf
from bot.states import FilesMenuStatesGroup


def files_router() -> Router:
    router = Router()

    # Menu block.
    router.message.register(menu, LocalizedTextFilter("files-menu-button"), AuthorizedFilter())

    # Cancel block.
    router.callback_query.register(
        cancel_callback,
        cdf.FilesData.filter(F.action == cdf.FilesActions.CANCEL),
        MsgAuthorFilter(),
    )
    router.message.register(
        cancel_message,
        FilesMenuStatesGroup.UPLOAD,
        LocalizedTextFilter("stop-button"),
    )
    router.message.register(
        cancel_message,
        FilesMenuStatesGroup.MKDIR,
        LocalizedTextFilter("cancel-button"),
    )

    # Upload block.
    router.callback_query.register(
        upload_start,
        cdf.FilesData.filter(F.action == cdf.FilesActions.UPLOAD),
        MsgAuthorFilter(),
    )
    router.message.register(
        upload,
        FilesMenuStatesGroup.UPLOAD,
        F.content_type == ContentType.DOCUMENT,
    )
    router.message.register(
        upload_incorrectly,
        FilesMenuStatesGroup.UPLOAD,
    )

    # Mkdir block.
    router.callback_query.register(
        start_mkdir,
        cdf.FilesData.filter(F.action == cdf.FilesActions.MKDIR),
        MsgAuthorFilter(),
    )
    router.message.register(
        mkdir,
        FilesMenuStatesGroup.MKDIR,
        F.text.regexp(r'^[^\s\/:*?"<>|]+$'),
    )
    router.message.register(
        incorrectly_mkdir,
        FilesMenuStatesGroup.MKDIR,
    )

    # Pagination block.
    router.callback_query.register(
        pag,
        cdf.FilesData.filter(F.action.in_({cdf.FilesActions.PAG_BACK, cdf.FilesActions.PAG_NEXT})),
        MsgAuthorFilter(),
    )

    # Delete block.
    router.callback_query.register(
        delete,
        cdf.FilesData.filter(F.action == cdf.FilesActions.DELETE),
        MsgAuthorFilter(),
    )
    router.callback_query.register(
        delete_confirm,
        cdf.FilesData.filter(F.action == cdf.FilesActions.DELETE_CONFIRM),
        MsgAuthorFilter(),
    )

    # Download block.
    router.callback_query.register(
        download,
        cdf.FilesData.filter(F.action == cdf.FilesActions.DOWNLOAD),
        MsgAuthorFilter(),
    )

    # Select block.
    router.callback_query.register(
        select,
        cdf.FilesData.filter(F.action == cdf.FilesActions.SELECT),
        MsgAuthorFilter(),
    )

    # Back block.
    router.callback_query.register(
        back,
        cdf.FilesData.filter(F.action == cdf.FilesActions.BACK),
        MsgAuthorFilter(),
    )

    return router
