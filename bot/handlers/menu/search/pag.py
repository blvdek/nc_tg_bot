"""Handler with pagination for search results."""
from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_query_msg, get_search_msg
from bot.keyboards.callback_data_factories import SearchActions, SearchData
from bot.nextcloud import NCSrvFactory


@get_query_msg
async def pag(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: SearchData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Pagination for search results.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for the search result.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    class_ = NCSrvFactory.get("SearchService")
    srv = await class_.create_instance(nc, ["like", "name", f"%{callback_data.query}%"])

    page_num = int(callback_data.page)
    page = page_num + 1 if callback_data.action == SearchActions.PAG_NEXT else page_num - 1

    text, reply_markup = get_search_msg(i18n, callback_data.query, srv.fsnodes, query.from_user.id, page=page)
    with suppress(TelegramBadRequest):
        await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()
