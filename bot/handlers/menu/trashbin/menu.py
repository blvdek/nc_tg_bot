"""Trash bin menu handler."""
from aiogram.types import Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_msg_user, get_trashbin_msg
from bot.nextcloud import NCSrvFactory


@get_msg_user
async def menu(message: Message, msg_from_user: TgUser, i18n: I18nContext, nc: AsyncNextcloud) -> None:
    """Trash bin menu.

    Trash bin entry point.

    :param message: Message object.
    :param msg_from_user: User who sent the message.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, srv.get_size(), msg_from_user.id)
    await message.reply(text=text, reply_markup=reply_markup)
