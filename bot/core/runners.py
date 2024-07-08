"""Functions to handle bot startup, shutdown, and webhook operations."""

from aiogram import Bot, Dispatcher, loggers
from aiogram.enums import MenuButtonType
from aiogram.types import BotCommand, MenuButtonWebApp, WebAppInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from aiohttp import web

from bot.core.config import settings
from bot.handlers import routers
from bot.middlewares import LocaleManager, QueryMsgMD


async def _set_bot_menu(bot: Bot) -> None:
    if settings.nc.overwrite and settings.nc.overwrite.protocol == "https":
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                type=MenuButtonType.WEB_APP,
                text="Nextcloud",
                web_app=WebAppInfo(
                    url=f"{settings.nc.overwrite.protocol}://{settings.nc.overwrite.host}:{settings.nc.overwrite.port}",
                ),
            ),
        )

    commands = [
        BotCommand(command="help", description="Get message with help text"),
        BotCommand(command="auth", description="Start authentification in Nextcloud"),
        BotCommand(command="logout", description="Logout from Nextcloud"),
    ]

    await bot.set_my_commands(commands)


async def on_startup(dispatcher: Dispatcher, bot: Bot) -> None:
    """Initializes the bot by setting up handlers, middleware, and registering bot commands.

    :param dispatcher: Aiogram dispatcher instance.
    :param bot: Aiogram bot instance.
    """
    loggers.dispatcher.info("Bot starting...")

    await _set_bot_menu(bot)

    for router in routers:
        dispatcher.include_router(router())

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="./bot/locales/{locale}/"),
        manager=LocaleManager(),
    )
    i18n_middleware.setup(dispatcher=dispatcher)
    dispatcher.callback_query.middleware.register(QueryMsgMD())

    loggers.dispatcher.info("Bot started.")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """Performs necessary cleanup when the bot is shutting down.

    :param dispatcher: Aiogram dispatcher instance.
    :param bot: Aiogram bot instance.
    """
    loggers.dispatcher.info("Bot stopping...")

    await dispatcher.storage.close()
    await dispatcher.fsm.storage.close()

    await bot.delete_webhook(drop_pending_updates=settings.tg.drop_pending_updates)
    await bot.session.close()

    loggers.dispatcher.info("Bot stopped.")


async def webhook_startup(
    dispatcher: Dispatcher,
    bot: Bot,
    url: str,
    secret: str | None = None,
) -> None:
    """Registers the bot's webhook with Telegram.

    :param dispatcher: Aiogram dispatcher instance.
    :param bot: Aiogram bot instance.
    :param url: The base URL for the webhook endpoint.
    :param secret: A secret token used for webhook verification, defaults to None.
    """
    if await bot.set_webhook(
        url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=secret,
    ):
        loggers.webhook.info(f"Bot webhook successfully set on {url}.")
        return
    loggers.webhook.info(f"Failed to set bot webhook on url {url}.")


async def webhook_shutdown(bot: Bot) -> None:
    """Deregisters the webhook and closes the bot session.

    :param bot: Aiogram bot instance.
    """
    if await bot.delete_webhook():
        loggers.webhook.info("Dropped bot webhook.")
    else:
        loggers.webhook.error("Failed to drop bot webhook.")
    await bot.session.close()


async def webhook_run(
    dp: Dispatcher,
    bot: Bot,
    path: str,
    host: str,
    port: int,
    secret: str | None = None,
) -> None:
    """Sets up and starts the webhook server for receiving updates via HTTP requests.

    :param dispatcher: Aiogram dispatcher instance.
    :param bot: Aiogram bot instance.
    :param path: The path under which the webhook endpoint is accessible.
    :param host: The hostname where the webhook should be hosted
    :param port: The port number on which the webhook server listens.
    :param secret: A secret token used for webhook verification, defaults to None.
    """
    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=secret,
    ).register(app, path=path)

    setup_application(app, dp, bot=bot)

    app.update(**dp.workflow_data, bot=bot)
    dp.startup.register(webhook_startup)
    dp.shutdown.register(webhook_shutdown)

    web.run_app(app=app, host=host, port=port)
