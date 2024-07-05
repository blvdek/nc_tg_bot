"""Handlers of actions that can be performed on a fsnodes from the trash bin."""
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_query_msg, get_trashbin_msg
from bot.keyboards import trashbin_fsnode_board
from bot.keyboards.callback_data_factories import TrashbinFsNodeData
from bot.nextcloud import NCSrvFactory


@get_query_msg
async def select(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
) -> None:
    """Offer actions that can be performed on the selected file from the trash bin.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    text = i18n.get("trashbin-fsnode")
    reply_markup = trashbin_fsnode_board(query.from_user.id, callback_data.file_id, callback_data.page)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()


@get_query_msg
async def delete(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Delete a file from the trash bin.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    await srv.delete(callback_data.file_id)

    await query.answer(i18n.get("trashbin-delete-alert"), show_alert=True)

    text, reply_markup = get_trashbin_msg(
        i18n,
        srv.trashbin,
        srv.get_size(),
        query.from_user.id,
        page=callback_data.page,
    )
    await query_msg.edit_text(text=text, reply_markup=reply_markup)


@get_query_msg
async def restore(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Restore a file from the trash bin.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    await srv.restore(callback_data.file_id)

    await query.answer(i18n.get("trashbin-restore-alert"), show_alert=True)

    text, reply_markup = get_trashbin_msg(
        i18n,
        srv.trashbin,
        srv.get_size(),
        query.from_user.id,
        page=callback_data.page,
    )
    await query_msg.edit_text(text=text, reply_markup=reply_markup)
