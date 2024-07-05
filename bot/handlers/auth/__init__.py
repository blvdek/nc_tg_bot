"""Router with authentication message."""

from aiogram import Router
from aiogram.filters.command import Command

from .auth import auth
from bot.middlewares import NextcloudMD, UnitOfWorkMD


def auth_router() -> Router:
    """Build router with authentication message.

    :return: Router with authentication message.
    """
    router = Router()

    router.message.outer_middleware(UnitOfWorkMD())
    router.message.outer_middleware(NextcloudMD())

    router.message.register(auth, Command("auth"))

    return router
