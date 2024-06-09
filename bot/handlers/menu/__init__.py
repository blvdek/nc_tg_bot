"""Menu router."""

from aiogram import F, Router
from aiogram.filters.command import Command

from .files import files_router
from .logout import logout, logout_cancel, logout_confirm
from bot import filters, middlewares
from bot.keyboards.callback_data_factories import LogoutActions, LogoutData


def menu_router() -> Router:
    router = Router()
    router.include_router(files_router())

    router.message.outer_middleware.register(middlewares.DatabaseMD())
    router.message.outer_middleware.register(middlewares.NextcloudMD())
    router.callback_query.outer_middleware.register(middlewares.DatabaseMD())
    router.callback_query.outer_middleware.register(middlewares.NextcloudMD())

    router.message.register(logout, Command("logout"), filters.AuthorizedFilter())
    router.callback_query.register(logout_confirm, LogoutData.filter(F.action == LogoutActions.CONFIRM))
    router.callback_query.register(logout_cancel, LogoutData.filter(F.action == LogoutActions.DENY))

    return router
