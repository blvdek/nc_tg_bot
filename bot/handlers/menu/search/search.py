from typing import cast

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_search_msg, validate_msg_text, validate_msg_user
from bot.nextcloud import NCSrvFactory
from bot.states import SearchStatesGroup


async def start_search(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    await state.set_state(SearchStatesGroup.SEARCH)

    text = i18n.get("search-enter")
    await message.reply(text=text)


@validate_msg_user
@validate_msg_text
async def search(message: Message, state: FSMContext, i18n: I18nContext, nc: AsyncNextcloud) -> None:
    msg_user = cast(User, message.from_user)
    msg_text = cast(str, message.text)

    await state.clear()

    class_ = NCSrvFactory.get("SearchService")
    srv = await class_.create_instance(nc, ["like", "name", f"%{message.text}%"])

    text, reply_markup = get_search_msg(i18n, msg_text, srv.fsnodes, msg_user.id)
    await message.reply(text=text, reply_markup=reply_markup)
