"""Cancel operation with fsnode handlers."""

from contextlib import suppress
from typing import cast

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg
from bot.keyboards import menu_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import FsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError


async def cancel_callback(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Cancel operation with fsnode in callback form.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    await state.clear()

    try:
        srv = await FsNodeService.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        return await query_msg.edit_text(text=i18n.get("fsnode-not-found"))

    text, reply_markup = get_fsnode_msg(
        i18n,
        srv.fsnode,
        srv.attached_fsnodes,
        query.from_user.id,
        page=callback_data.page,
    )
    with suppress(TelegramBadRequest):
        msg = await query_msg.edit_text(text=text, reply_markup=reply_markup)
    return msg


async def cancel_message(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message:
    """Cancel operation with fsnode in message form.

    :param message: Message object.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: AsyncNextcloud.
    """
    msg_from_user = cast(TgUser, message.from_user)
    data = await state.get_data()

    try:
        srv = await FsNodeService.create_instance(nc, file_id=data["file_id"])
    except FsNodeNotFoundError:
        return await message.reply(text=i18n.get("fsnode-not-found"))

    await state.clear()

    menu_reply_markup = menu_board()
    menu_text = i18n.get("cancel")
    await message.reply(text=menu_text, reply_markup=menu_reply_markup)

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, msg_from_user.id)
    return await message.reply(text=text, reply_markup=reply_markup)
