"""Fsnode menu handler."""
from aiogram.types import Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg, get_msg_user
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError


@get_msg_user
async def menu(message: Message, msg_from_user: TgUser, i18n: I18nContext, nc: AsyncNextcloud) -> None:
    """Fsnode menu.

    Fsnode entry point.

    :param message: Message object.
    :param msg_from_user: User who sent the message.
    :param i18n: Internationalization context.
    :param nc: AsyncNextcloud.
    """
    try:
        class_ = NCSrvFactory.get("RootFsNodeService")
        srv = await class_.create_instance(nc)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await message.reply(text=text)
        return

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, msg_from_user.id)
    await message.reply(text=text, reply_markup=reply_markup)
