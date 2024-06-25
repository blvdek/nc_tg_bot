"""Menu router."""

from aiogram import F, Router
from aiogram_i18n import LazyFilter

from .cancel import cancel_callback
from .cleanup import cleanup, cleanup_confirm
from .fsnode import delete, restore, select
from .menu import menu
from .pag import pag
from bot.filters import AuthorizedFilter, MsgAuthorFilter
from bot.keyboards.callback_data_factories import (
    TrashbinActions,
    TrashbinData,
    TrashbinFsNodeActions,
    TrashbinFsNodeData,
)


def trashbin_router() -> Router:
    router = Router()

    router.message.register(menu, LazyFilter("trashbin-button"), AuthorizedFilter())

    router.callback_query.register(select, TrashbinFsNodeData.filter(F.action == TrashbinFsNodeActions.SELECT))
    router.callback_query.register(delete, TrashbinFsNodeData.filter(F.action == TrashbinFsNodeActions.DELETE))
    router.callback_query.register(restore, TrashbinFsNodeData.filter(F.action == TrashbinFsNodeActions.RESTORE))

    router.callback_query.register(cancel_callback, TrashbinData.filter(F.action == TrashbinActions.CANCEL))

    router.callback_query.register(cleanup, TrashbinData.filter(F.action == TrashbinActions.CLEANUP))
    router.callback_query.register(cleanup_confirm, TrashbinData.filter(F.action == TrashbinActions.CLEANUP_CONFIRM))

    router.callback_query.register(
        pag,
        TrashbinData.filter(F.action.in_({TrashbinActions.PAG_BACK, TrashbinActions.PAG_NEXT})),
        MsgAuthorFilter(TrashbinData),
    )

    return router
