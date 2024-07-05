"""Cancel operation with fsnode handlers."""
from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg, get_msg_user, get_query_msg
from bot.keyboards import menu_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError


@get_query_msg
async def cancel_callback(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Cancel operation with fsnode in callback form.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    await state.clear()

    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    text, reply_markup = get_fsnode_msg(
        i18n,
        srv.fsnode,
        srv.attached_fsnodes,
        query.from_user.id,
        page=callback_data.page,
    )
    with suppress(TelegramBadRequest):
        await query_msg.edit_text(text=text, reply_markup=reply_markup)
    await query.answer()


@get_msg_user
async def cancel_message(
    message: Message,
    msg_from_user: TgUser,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Cancel operation with fsnode in message form.

    :param message: Message object.
    :param msg_from_user: User who sent the message.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: AsyncNextcloud.
    """
    data = await state.get_data()

    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=data["file_id"])
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await message.reply(text=text)
        return

    await state.clear()

    menu_reply_markup = menu_board()
    menu_text = i18n.get("cancel")
    await message.reply(text=menu_text, reply_markup=menu_reply_markup)

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, msg_from_user.id)
    with suppress(TelegramBadRequest):
        await message.answer(text=text, reply_markup=reply_markup)
