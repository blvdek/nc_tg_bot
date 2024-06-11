"""Authentication router."""

from aiogram import Router
from aiogram.filters.command import Command

from .auth import auth
from bot.middlewares import UnitOfWorkMD, NextcloudMD


def auth_router() -> Router:
    router = Router()

    router.message.outer_middleware(UnitOfWorkMD())
    router.message.outer_middleware(NextcloudMD())

    router.message.register(auth, Command("auth"))

    return router
