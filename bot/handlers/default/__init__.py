from aiogram import Router
from aiogram.filters.command import Command

from .start import start
from bot import middlewares


def default_router() -> Router:
    router = Router()

    router.message.outer_middleware(middlewares.DatabaseMD())

    router.message.register(start, Command("start"))

    return router
