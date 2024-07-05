"""Search handlers."""
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_msg_text, get_msg_user, get_search_msg
from bot.nextcloud import NCSrvFactory
from bot.states import SearchStatesGroup


async def start_search(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """Initiate search process and ask user for the search text.

    Search entry point.

    :param message: Message object.
    :param state: State machine context.
    :param i18n: Internationalization context.
    """
    await state.set_state(SearchStatesGroup.SEARCH)

    text = i18n.get("search-enter")
    await message.reply(text=text)


@get_msg_user
@get_msg_text
async def search(
    message: Message,
    msg_from_user: TgUser,
    msg_text: str,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Search for files in the Nextcloud instance based on the given search text.

    :param message: Message object.
    :param msg_from_user: User who sent the message.
    :param msg_text: Text of the message, as well as the search text.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    await state.clear()

    class_ = NCSrvFactory.get("SearchService")
    srv = await class_.create_instance(nc, ["like", "name", f"%{message.text}%"])

    text, reply_markup = get_search_msg(i18n, msg_text, srv.fsnodes, msg_from_user.id)
    await message.reply(text=text, reply_markup=reply_markup)
