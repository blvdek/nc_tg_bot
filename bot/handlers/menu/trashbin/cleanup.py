"""Cleanup handlers."""

from typing import cast

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.keyboards import trashbin_cleanup_board
from bot.keyboards.callback_data_factories import TrashbinData
from bot.nextcloud import TrashbinService


async def cleanup(
    query: CallbackQuery,
    callback_data: TrashbinData,
    i18n: I18nContext,
) -> Message | bool:
    """Ask confirmation to cleanup trash bin.

    :param query: Callback query object.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    query_msg = cast(Message, query.message)

    reply_markup = trashbin_cleanup_board(query.from_user.id, callback_data.page)
    return await query_msg.edit_text(
        text=i18n.get("trashbin-cleanup-start"),
        reply_markup=reply_markup,
    )


async def cleanup_confirm(
    query: CallbackQuery,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Cleanup the trash bin.

    :param query: Callback query object.    query_msg = cast(Message, query.message)
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    """
    query_msg = cast(Message, query.message)

    srv = await TrashbinService.create_instance(nc)

    await srv.cleanup()

    return await query_msg.edit_text(text=i18n.get("trashbin-empty"))
