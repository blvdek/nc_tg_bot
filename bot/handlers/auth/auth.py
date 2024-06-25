"""Authentication in Nextcloud handler."""
from typing import cast

from aiogram import Bot
from aiogram.enums import MenuButtonType
from aiogram.types import MenuButtonWebApp, Message, WebAppInfo
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud, NextcloudException

from bot.core import settings
from bot.db import UnitOfWork
from bot.db.models import User
from bot.handlers._core import validate_msg_user
from bot.keyboards import menu_board

AUTH_TIMEOUT = 60 * 20
AUTH_TIMEOUT_IN_MIN = AUTH_TIMEOUT // 60


@validate_msg_user
async def auth(
    message: Message,
    bot: Bot,
    i18n: I18nContext,
    nc: AsyncNextcloud,
    uow: UnitOfWork,
) -> None:
    msg_user = cast(TgUser, message.from_user)

    if await uow.users.get_by_id(msg_user.id):
        text = i18n.get("already-authorized")
        reply_markup = menu_board()
        await message.reply(text=text, reply_markup=reply_markup)
        return

    init = await nc.loginflow_v2.init(user_agent=settings.appname)
    url_text = init.login
    if not init.login.startswith("https"):
        url_text = f"<code>{url_text}</code>"
    text = i18n.get("auth-init", url=url_text, timeout=AUTH_TIMEOUT_IN_MIN)
    init_message = await message.reply(text=text)

    try:
        credentials = await nc.loginflow_v2.poll(token=init.token, timeout=AUTH_TIMEOUT)
    except NextcloudException:
        text = i18n.get("auth-timeout")
        await init_message.edit_text(text=text)
        return

    user = User(
        id=msg_user.id,
        nc_login=credentials.login_name,
        nc_app_password=credentials.app_password,
        name=msg_user.username,
        first_name=msg_user.first_name,
        last_name=msg_user.last_name,
    )
    await uow.users.add(user)
    await uow.commit()

    if credentials.server.startswith("https"):
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                type=MenuButtonType.WEB_APP,
                text="Nextcloud",
                web_app=WebAppInfo(url=credentials.server),
            ),
        )

    text = i18n.get("auth-success")
    await init_message.edit_text(text)

    text = i18n.get("auth-welcome")
    reply_markup = menu_board()
    await message.reply(text=text, reply_markup=reply_markup)
