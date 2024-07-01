
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_query_msg, get_trashbin_msg
from bot.keyboards.callback_data_factories import TrashbinActions, TrashbinData
from bot.nextcloud import NCSrvFactory


@get_query_msg
async def pag(
    query: CallbackQuery,
    query_msg: Message,
    i18n: I18nContext,
    callback_data: TrashbinData,
    nc: AsyncNextcloud,
) -> None:
    page_num = int(callback_data.page)
    page = page_num + 1 if callback_data.action == TrashbinActions.PAG_NEXT else page_num - 1

    class_ = NCSrvFactory.get("TrashbinService")
    srv = await class_.create_instance(nc)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, srv.get_size(), query.from_user.id, page=page)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()
