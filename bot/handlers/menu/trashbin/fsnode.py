from typing import cast

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_trashbin_msg, validate_query_msg
from bot.keyboards import trashbin_fsnode_board
from bot.keyboards.callback_data_factories import TrashbinFsNodeData
from bot.nextcloud import NCSrvFactory


@validate_query_msg
async def select(
    query: CallbackQuery,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
) -> None:
    query_msg = cast(Message, query.message)

    text = i18n.get("trashbin-fsnode")
    reply_markup = trashbin_fsnode_board(query.from_user.id, callback_data.file_id, callback_data.page)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()


@validate_query_msg
async def delete(
    query: CallbackQuery,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    query_msg = cast(Message, query.message)

    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    await srv.delete(callback_data.file_id)

    await query.answer(i18n.get("trashbin-delete-alert"), show_alert=True)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, query.from_user.id, page=callback_data.page)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)


@validate_query_msg
async def restore(
    query: CallbackQuery,
    callback_data: TrashbinFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    query_msg = cast(Message, query.message)

    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    await srv.restore(callback_data.file_id)

    await query.answer(i18n.get("trashbin-restore-alert"), show_alert=True)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, query.from_user.id, page=callback_data.page)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)
