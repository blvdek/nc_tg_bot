"""Authentication in Nextcloud handler."""

from typing import cast
from urllib.parse import urlparse

from aiogram.types import Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud, NextcloudException

from bot.core import settings
from bot.db import UnitOfWork
from bot.db.models import User
from bot.keyboards import menu_board

AUTH_TIMEOUT = 60 * 20
AUTH_TIMEOUT_IN_MIN = AUTH_TIMEOUT // 60


async def auth(
    message: Message,
    i18n: I18nContext,
    nc: AsyncNextcloud,
    uow: UnitOfWork,
) -> Message | bool:
    """Authenticate a user in Nextcloud.

    Initialize the login flow, polling for credentials, and add user to the database.

    :param message: Message object.
    :param msg_from_user: User who sent the message.
    :param bot: Bot object.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    :param uow: Unit of work.
    """
    msg_from_user = cast(TgUser, message.from_user)

    if await uow.users.get_by_id(msg_from_user.id):
        text = i18n.get("already-authorized")
        reply_markup = menu_board()
        return await message.reply(text=text, reply_markup=reply_markup)

    init = await nc.loginflow_v2.init(user_agent=settings.appname)
    url = init.login

    if settings.nc.public_host:
        parsed_url = urlparse(url)
        url = parsed_url._replace(
            scheme=settings.nc.public_protocol, netloc=settings.nc.public_host,
        ).geturl()

    if not url.startswith("https"):
        url = f"<code>{url}</code>"
    text = i18n.get("auth-init", url=url, timeout=AUTH_TIMEOUT_IN_MIN)
    init_message = await message.reply(text=text)

    try:
        credentials = await nc.loginflow_v2.poll(token=init.token, timeout=AUTH_TIMEOUT)
    except NextcloudException:
        text = i18n.get("auth-timeout")
        return await init_message.edit_text(text=text)

    user = User(
        id=msg_from_user.id,
        nc_login=credentials.login_name,
        nc_app_password=credentials.app_password,
        name=msg_from_user.username,
        first_name=msg_from_user.first_name,
        last_name=msg_from_user.last_name,
    )
    await uow.users.add(user)
    await uow.commit()

    text = i18n.get("auth-success")
    await init_message.edit_text(text)

    text = i18n.get("auth-welcome")
    reply_markup = menu_board()
    return await message.reply(text=text, reply_markup=reply_markup)
