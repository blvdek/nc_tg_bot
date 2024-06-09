"""Authentication router."""

from aiogram import Router
from aiogram.filters.command import Command

from .auth import auth
from bot import middlewares


def auth_router() -> Router:
    router = Router()

    router.message.outer_middleware(middlewares.DatabaseMD())
    router.message.outer_middleware(middlewares.NextcloudMD())

    router.message.register(auth, Command("auth"))

    return router
