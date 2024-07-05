"""File or directory creation handlers."""

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Document, Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext, LazyProxy
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.handlers._core import (
    get_fsnode_msg,
    get_human_readable_bytes,
    get_msg_doc,
    get_msg_text,
    get_msg_user,
    get_query_msg,
)
from bot.keyboards import fsnode_new_board, menu_board, reply_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError
from bot.states import FsNodeMenuStatesGroup


@get_query_msg
async def new(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Creating a new file or directory menu.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    reply_markup = fsnode_new_board(
        fsnode=srv.fsnode,
        from_user_id=query.from_user.id,
        page=callback_data.page,
    )
    text = i18n.get("fsnode-new", name=srv.fsnode.name)
    await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()


@get_query_msg
async def upload_start(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
) -> None:
    """Initiate file upload to Nextcloud process.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param state: State machine context.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    await state.set_state(FsNodeMenuStatesGroup.UPLOAD)
    await state.update_data(file_id=callback_data.file_id)

    reply_markup = reply_board(
        LazyProxy("stop-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    text = i18n.get("fsnode-upload-start")
    await query_msg.answer(text=text, reply_markup=reply_markup)

    await query.answer()


@get_msg_doc
async def upload(
    message: Message,
    msg_doc: Document,
    bot: Bot,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Upload a file to the Nextcloud server.

    Set state to UPLOAD status and start waiting message with pinned documents to upload to Nextcloud or cancel message.

    :param message: Message object.
    :param msg_doc: Telegram document object.
    :param bot: Bot object.
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

    if msg_doc.file_size is None or msg_doc.file_size == 0:
        text = i18n.get("fsnode-empty")
        await message.answer(text=text)
        return
    if msg_doc.file_size > settings.tg.max_upload_size:
        text = i18n.get(
            "fsnode-size-limit",
            size=get_human_readable_bytes(msg_doc.file_size),
            size_limit=get_human_readable_bytes(settings.tg.max_upload_size),
        )
        await message.answer(text=text)
        return

    tg_file_obj = await bot.get_file(msg_doc.file_id)
    if tg_file_obj.file_path is None:
        text = i18n.get("fsnode-upload-error")
        await message.reply(text=text)
        return

    buff = await bot.download_file(tg_file_obj.file_path, chunk_size=settings.nc.chunksize)
    await srv.upload(buff, msg_doc.file_name)

    text = i18n.get("fsnode-upload-success", name=msg_doc.file_name)
    await message.reply(text=text)


@get_query_msg
async def mkdir_start(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
) -> None:
    """Initiate creation of a new directory on Netxcloud server.

    Set state to MKDIR status and start waiting message with name for new directory or cancel message.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param state: State machine context.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    """
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
    msg_from_user: TgUser,
    msg_text: str,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Create a new directory on Nextcloud server.

    End process after creation.

    :param message: Message object.
    :param msg_from_user: User who sent the message.
    :param msg_text: Text of the message, as well as the search text.
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

    new_dir = await srv.mkdir(msg_text)

    menu_reply_markup = menu_board()
    menu_text = i18n.get("fsnode-mkdir-success", name=new_dir.name)
    await message.reply(text=menu_text, reply_markup=menu_reply_markup)

    await state.clear()

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, msg_from_user.id)
    await message.reply(text=text, reply_markup=reply_markup)


async def upload_incorrectly(message: Message, i18n: I18nContext) -> None:
    """File for uploading to the server is incorrectly.

    :param message: Message object.
    :param i18n: Internationalization context.
    """
    text = i18n.get("fsnode-upload-incorrectly")
    await message.reply(text=text)


async def incorrectly_mkdir(message: Message, i18n: I18nContext) -> None:
    """Name for directory is incorrectly.

    :param message: Message object.
    :param i18n: Internationalization context.
    """
    text = i18n.get("fsnode-mkdir-incorrectly")
    await message.reply(text=text)
