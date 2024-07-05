"""Module for launching the bot.

This module handles the initialization and control flow of the bot, including setting up logging,
launching the asynchronous event loop via uvloop, and registering event handlers for startup and shutdown events.
"""

import logging

import uvloop

from bot.core import bot, dp, on_shutdown, on_startup, settings, webhook_run


async def main() -> None:
    """Asynchronous entry point for the application.

    This function initializes the bot, registers event handlers, and starts the polling process or webhook,
    depending on the configuration settings.
    """
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    if settings.webhook:
        await webhook_run(
            dp,
            bot,
            settings.webhook.path,
            settings.webhook.host,
            settings.webhook.port,
            settings.webhook.secret,
        )
        return
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(settings.logging))

    uvloop.run(main())
