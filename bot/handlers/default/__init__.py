from aiogram import Router
from aiogram.filters.command import Command

from .default import help_msg, start


def default_router() -> Router:
    router = Router()

    router.message.register(start, Command("start"))
    router.message.register(help_msg, Command("help"))

    return router
