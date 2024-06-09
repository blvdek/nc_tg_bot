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
from bot import filters
from bot.keyboards.callback_data_factories import FilesMenuActions, FilesMenuData
from bot.states import FilesMenuStatesGroup


def files_router() -> Router:
    router = Router()

    router.message.register(menu, filters.LocalizedTextFilter("files-menu-button"), filters.AuthorizedFilter())

    router.message.register(cancel_message, FilesMenuStatesGroup.MKDIR, filters.LocalizedTextFilter("cancel-button"))
    router.message.register(cancel_message, FilesMenuStatesGroup.UPLOAD, filters.LocalizedTextFilter("cancel-button"))
    router.callback_query.register(cancel_callback, FilesMenuData.filter(F.action == FilesMenuActions.CANCEL))

    router.callback_query.register(upload_start, FilesMenuData.filter(F.action == FilesMenuActions.UPLOAD))
    router.message.register(upload, FilesMenuStatesGroup.UPLOAD, F.content_type == ContentType.DOCUMENT)
    router.message.register(upload_incorrectly, FilesMenuStatesGroup.UPLOAD)

    router.callback_query.register(start_mkdir, FilesMenuData.filter(F.action == FilesMenuActions.MKDIR))
    router.message.register(mkdir, FilesMenuStatesGroup.MKDIR, F.text.regexp(r'^[^\s\/:*?"<>|]+$'))
    router.message.register(incorrectly_mkdir, FilesMenuStatesGroup.MKDIR)

    router.callback_query.register(
        pag,
        FilesMenuData.filter(F.action.in_({FilesMenuActions.PAG_BACK, FilesMenuActions.PAG_NEXT})),
    )

    router.callback_query.register(delete, FilesMenuData.filter(F.action == FilesMenuActions.DELETE))
    router.callback_query.register(delete_confirm, FilesMenuData.filter(F.action == FilesMenuActions.DELETE_CONFIRM))

    router.callback_query.register(download, FilesMenuData.filter(F.action == FilesMenuActions.DOWNLOAD))

    router.callback_query.register(select, FilesMenuData.filter(F.action == FilesMenuActions.SELECT))

    router.callback_query.register(back, FilesMenuData.filter(F.action == FilesMenuActions.BACK))

    return router
