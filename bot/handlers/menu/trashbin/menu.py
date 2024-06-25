from typing import cast

from aiogram.types import Message, User
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_trashbin_msg, validate_msg_user
from bot.nextcloud import NCSrvFactory


@validate_msg_user
async def menu(message: Message, i18n: I18nContext, nc: AsyncNextcloud) -> None:
    user = cast(User, message.from_user)

    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, user.id)
    await message.reply(text=text, reply_markup=reply_markup)
