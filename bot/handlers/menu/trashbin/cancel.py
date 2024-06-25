from typing import cast

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_trashbin_msg, validate_query_msg
from bot.keyboards.callback_data_factories import TrashbinData
from bot.nextcloud import NCSrvFactory


@validate_query_msg
async def cancel_callback(
    query: CallbackQuery,
    callback_data: TrashbinData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    query_msg = cast(Message, query.message)

    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, query.from_user.id, page=callback_data.page)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()
