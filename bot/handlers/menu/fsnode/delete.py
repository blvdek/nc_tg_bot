"""Fsnode delete handlers."""
from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg, get_query_msg
from bot.keyboards import fsnode_delete_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError


@get_query_msg
async def delete(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Ask confirmation to delete fsnode.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    reply_markup = fsnode_delete_board(
        fsnode=srv.fsnode,
        from_user_id=query.from_user.id,
        page=callback_data.page,
    )
    text = i18n.get("fsnode-delete", name=srv.fsnode.name)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()


@get_query_msg
async def delete_confirm(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Delete fsnode.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
        class_ = NCSrvFactory.get("PrevFsNodeService")
        prev_srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    await srv.delete()
    prev_srv.attached_fsnodes.remove(srv.fsnode)

    text, reply_markup = get_fsnode_msg(
        i18n,
        prev_srv.fsnode,
        prev_srv.attached_fsnodes,
        query.from_user.id,
        page=callback_data.page,
    )
    with suppress(TelegramBadRequest):
        await query_msg.edit_text(text=text, reply_markup=reply_markup)

    text = i18n.get("fsnode-delete-alert")
    await query.answer(text=text, show_alert=True)
