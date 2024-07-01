from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_msg_text, get_msg_user, get_search_msg
from bot.nextcloud import NCSrvFactory
from bot.states import SearchStatesGroup

from rich import print


async def start_search(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    await state.set_state(SearchStatesGroup.SEARCH)

    text = i18n.get("search-enter")
    await message.reply(text=text)


@get_msg_user
@get_msg_text
async def search(
    message: Message,
    msg_user: TgUser,
    msg_text: str,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    await state.clear()

    class_ = NCSrvFactory.get("SearchService")
    srv = await class_.create_instance(nc, ["like", "name", f"%{message.text}%"])

    text, reply_markup = get_search_msg(i18n, msg_text, srv.fsnodes, msg_user.id)
    await message.reply(text=text, reply_markup=reply_markup)
