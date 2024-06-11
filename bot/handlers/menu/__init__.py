"""Menu router."""

from aiogram import F, Router
from aiogram.filters.command import Command

from .files import files_router
from .logout import logout, logout_cancel, logout_confirm
from bot.filters import AuthorizedFilter
from bot.keyboards.callback_data_factories import LogoutActions, LogoutData
from bot.middlewares import UnitOfWorkMD, NextcloudMD


def menu_router() -> Router:
    router = Router()
    router.include_router(files_router())

    router.message.outer_middleware.register(UnitOfWorkMD())
    router.message.outer_middleware.register(NextcloudMD())
    router.callback_query.outer_middleware.register(UnitOfWorkMD())
    router.callback_query.outer_middleware.register(NextcloudMD())

    router.message.register(logout, Command("logout"), AuthorizedFilter())
    router.callback_query.register(logout_confirm, LogoutData.filter(F.action == LogoutActions.CONFIRM))
    router.callback_query.register(logout_cancel, LogoutData.filter(F.action == LogoutActions.DENY))

    return router
