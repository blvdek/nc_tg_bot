"""Router with main menu messages and main menu partitions routers."""

from aiogram import F, Router
from aiogram.filters.command import Command

from .fsnode import fsnode_menu_router
from .logout import logout, logout_cancel, logout_confirm
from .search import search_router
from .trashbin import trashbin_router
from bot.filters import AuthorizedFilter, OnlyPrivateFilter
from bot.keyboards.callback_data_factories import LogoutActions, LogoutData
from bot.middlewares import NextcloudMD, UnitOfWorkMD


def menu_router() -> Router:
    """Build router with main menu messages and main menu partitions routers.

    :return: Router with main menu messages and main menu partitions routers.
    """
    router = Router()
    router.include_router(fsnode_menu_router())
    router.include_router(trashbin_router())
    router.include_router(search_router())

    router.message.outer_middleware.register(UnitOfWorkMD())
    router.message.outer_middleware.register(NextcloudMD())
    router.callback_query.outer_middleware.register(UnitOfWorkMD())
    router.callback_query.outer_middleware.register(NextcloudMD())

    router.message.register(logout, Command("logout"), AuthorizedFilter(), OnlyPrivateFilter())
    router.callback_query.register(
        logout_confirm,
        LogoutData.filter(F.action == LogoutActions.CONFIRM),
    )
    router.callback_query.register(
        logout_cancel,
        LogoutData.filter(F.action == LogoutActions.DENY),
    )

    return router
