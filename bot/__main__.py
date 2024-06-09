"""Startup and shutdown bot logick."""

import asyncio
import logging

import uvloop
from aiogram.enums import MenuButtonType
from aiogram.types import BotCommand, MenuButtonWebApp, WebAppInfo
from rich.logging import RichHandler

from bot.core import bot, dp, settings
from bot.handlers import routers
from bot.middlewares import TranslatorMD

if settings.webhook:
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    from aiohttp import web


async def on_startup() -> None:
    """Register routers, middlewares, commands and changes the menu button on startup."""
    logger.info("Bot starting...")

    for router in routers:
        dp.include_router(router())

    dp.message.outer_middleware(TranslatorMD())
    dp.callback_query.outer_middleware(TranslatorMD())

    if settings.nextcloud.domain and settings.nextcloud.domain.startswith("https"):
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                type=MenuButtonType.WEB_APP,
                text="Nextcloud",
                web_app=WebAppInfo(url=settings.nextcloud.domain_url),
            ),
        )

    commands = [
        BotCommand(command="help", description="Get message with help text"),
        BotCommand(command="auth", description="Start authentification in Nextcloud"),
        BotCommand(command="logout", description="Logout from Nextcloud"),
    ]
    await bot.set_my_commands(commands)

    logger.info("Bot started.")


async def on_shutdown() -> None:
    """Close storage, cache, webhook and telegram session on shutdown."""
    logger.info("Bot stopping...")

    await dp.storage.close()
    await dp.fsm.storage.close()

    await bot.delete_webhook()
    await bot.session.close()

    logger.info("Bot stopped.")


async def setup_webhook() -> None:
    """Set up a webhook for receiving updates from a Telegram.

    :raises NameError: If the webhook settings are not specified in the application's settings.
    """
    if settings.webhook:
        await bot.set_webhook(
            settings.webhook.url,
            allowed_updates=dp.resolve_used_update_types(),
            secret_token=settings.webhook.secret,
        )
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=settings.webhook.secret,
        )
        app = web.Application()
        webhook_requests_handler.register(app, path=settings.webhook.path)
        setup_application(app, dp, bot=bot)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=settings.webhook.host, port=settings.webhook.port)
        await site.start()

        await asyncio.Event().wait()
    else:
        msg = "The settings don't specify the data for connecting to the server to use the Webhook."
        raise NameError(msg)


async def main() -> None:
    """Entry point of bot."""
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    if settings.webhook:
        await setup_webhook()
    else:
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(settings.logging), handlers=(RichHandler(),))
    logger = logging.getLogger("aiogram.dispatcher")

    uvloop.run(main())
