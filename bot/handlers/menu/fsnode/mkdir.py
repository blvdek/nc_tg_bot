
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext, LazyProxy
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg, get_msg_text, get_msg_user, get_query_msg
from bot.keyboards import menu_board, reply_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError
from bot.states import FsNodeMenuStatesGroup


@get_query_msg
async def start_mkdir(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
) -> None:
    await state.set_state(FsNodeMenuStatesGroup.MKDIR)
    await state.update_data(file_id=callback_data.file_id)

    reply_markup = reply_board(
        LazyProxy("cancel-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    text = i18n.get("fsnode-mkdir-start")
    await query_msg.answer(text=text, reply_markup=reply_markup)

    await query.answer()


@get_msg_user
@get_msg_text
async def mkdir(
    message: Message,
    msg_user: TgUser,
    msg_text: str,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    data = await state.get_data()

    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=data["file_id"])
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await message.reply(text=text)
        return

    new_dir = await srv.mkdir(msg_text)

    menu_reply_markup = menu_board()
    menu_text = i18n.get("fsnode-mkdir-success", name=new_dir.name)
    await message.reply(text=menu_text, reply_markup=menu_reply_markup)

    await state.clear()

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, msg_user.id)
    await message.reply(text=text, reply_markup=reply_markup)


async def incorrectly_mkdir(message: Message, i18n: I18nContext) -> None:
    text = i18n.get("fsnode-mkdir-incorrectly")
    await message.reply(text=text)