"""Authentication in Nextcloud handler."""

from aiogram.types import Message
from nc_py_api import AsyncNextcloud, NextcloudException

from bot.core import settings
from bot.db import UnitOfWork
from bot.db.models import User
from bot.keyboards import menu_board
from bot.language import LocalizedTranslator

AUTH_TIMEOUT = 60 * 20
AUTH_TIMEOUT_IN_MIN = AUTH_TIMEOUT // 60


async def auth(
    message: Message,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
    uow: UnitOfWork,
) -> None:
    if message.from_user is None:
        text = translator.get("msg_is_inaccessible")
        await message.reply(text=text)
        return
    if await uow.users.get_by_id(message.from_user.id):
        text = translator.get("already-authorized")
        await message.reply(text=text)
        return

    init = await nc.loginflow_v2.init(user_agent=settings.appname)
    url_text = init.login
    if not init.login.startswith("https"):
        url_text = f"<code>{url_text}</code>"
    text = translator.get("auth-init", url=url_text, timeout=AUTH_TIMEOUT_IN_MIN)
    init_message = await message.reply(text=text)

    try:
        credentials = await nc.loginflow_v2.poll(token=init.token, timeout=AUTH_TIMEOUT)
    except NextcloudException:
        text = translator.get("auth-timeout")
        await init_message.edit_text(text=text)
        return

    user = User(
        id=message.from_user.id,
        nc_login=credentials.login_name,
        nc_app_password=credentials.app_password,
        name=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await uow.users.add(user)
    await uow.commit()

    text = translator.get("auth-success")
    await init_message.edit_text(text)

    text = translator.get("auth-welcome")
    reply_markup = menu_board(translator, is_persistent=True, resize_keyboard=True, selective=True)
    await message.reply(text=text, reply_markup=reply_markup)
