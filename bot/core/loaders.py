"""Build dispatcher logic and bot instance.

Build dispatcher and bot instance for the Nextcloud Telegram Bot, configuringthe
storage backend and integrating with the Telegram API.
"""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from bot.core.config import settings
from bot.db import session_maker

session = None
if settings.tg.api_server:
    session = AiohttpSession(api=TelegramAPIServer.from_base(settings.tg.api_server))

bot = Bot(token=settings.tg.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)

_storage = (
    RedisStorage(
        redis=Redis(
            db=settings.redis.db,
            host=settings.redis.host,
            password=settings.redis.password,
            username=settings.redis.user,
            port=settings.redis.port,
        ),
        state_ttl=settings.redis.state_ttl,
        data_ttl=settings.redis.data_ttl,
    )
    if settings.redis
    else MemoryStorage()
)

dp = Dispatcher(storage=_storage, _session_maker=session_maker)
