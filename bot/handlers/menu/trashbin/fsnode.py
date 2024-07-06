"""Handlers of actions that can be performed on a fsnodes from the trash bin."""

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_trashbin_msg
from bot.keyboards import trashbin_fsnode_board
from bot.keyboards.callback_data_factories import TrashbinFsNodeData
from bot.nextcloud import TrashbinService


async def select(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
) -> Message | bool:
    """Offer actions that can be performed on the selected file from the trash bin.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    reply_markup = trashbin_fsnode_board(
        query.from_user.id, callback_data.file_id, callback_data.page,
    )
    return await query_msg.edit_text(text=i18n.get("trashbin-fsnode"), reply_markup=reply_markup)


async def delete(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Delete a file from the trash bin.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    srv = await TrashbinService.create_instance(nc)

    await srv.delete(callback_data.file_id)

    await query.answer(i18n.get("trashbin-delete-alert"), show_alert=True)

    text, reply_markup = get_trashbin_msg(
        i18n,
        srv.trashbin,
        srv.get_size(),
        query.from_user.id,
        page=callback_data.page,
    )
    return await query_msg.edit_text(text=text, reply_markup=reply_markup)


async def restore(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Restore a file from the trash bin.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    srv = await TrashbinService.create_instance(nc)

    await srv.restore(callback_data.file_id)

    await query.answer(i18n.get("trashbin-restore-alert"), show_alert=True)

    text, reply_markup = get_trashbin_msg(
        i18n,
        srv.trashbin,
        srv.get_size(),
        query.from_user.id,
        page=callback_data.page,
    )
    return await query_msg.edit_text(text=text, reply_markup=reply_markup)
