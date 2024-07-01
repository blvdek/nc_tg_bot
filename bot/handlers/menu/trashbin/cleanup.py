
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_query_msg
from bot.keyboards import trashbin_cleanup_board
from bot.keyboards.callback_data_factories import TrashbinData
from bot.nextcloud import NCSrvFactory


@get_query_msg
async def cleanup(
    query: CallbackQuery,
    query_msg: Message,
    i18n: I18nContext,
    callback_data: TrashbinData,
) -> None:
    text = i18n.get("trashbin-cleanup-start")
    reply_markup = trashbin_cleanup_board(query.from_user.id, callback_data.page)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()


@get_query_msg
async def cleanup_confirm(
    query: CallbackQuery,
    query_msg: Message,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    await srv.cleanup()

    text = i18n.get("trashbin-empty")
    await query_msg.edit_text(text=text)

    await query.answer()
