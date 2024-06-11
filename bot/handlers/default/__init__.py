from aiogram import Router
from aiogram.filters.command import Command

from .start import start


def default_router() -> Router:
    router = Router()

    router.message.register(start, Command("start"))

    return router
