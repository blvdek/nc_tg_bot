from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext, LazyProxy
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.handlers._core import get_query_msg
from bot.keyboards import reply_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError
from bot.states import FsNodeMenuStatesGroup


@get_query_msg
async def upload_start(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
) -> None:
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


async def upload(
    message: Message,
    bot: Bot,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    if message.document is None:
        text = i18n.get("fsnode-upload-error")
        await message.reply(text=text)
        return

    data = await state.get_data()

    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=data["file_id"])
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await message.reply(text=text)
        return

    tg_file_obj = await bot.get_file(message.document.file_id)
    if tg_file_obj.file_path is None:
        text = i18n.get("fsnode-upload-error")
        await message.reply(text=text)
        return

    buff = await bot.download_file(tg_file_obj.file_path, chunk_size=settings.telegram.chunk_size)
    await srv.upload(buff, message.document.file_name)

    text = i18n.get("fsnode-upload-success", name=message.document.file_name)
    await message.reply(text=text)


async def upload_incorrectly(message: Message, i18n: I18nContext) -> None:
    text = i18n.get("fsnode-upload-incorrectly")
    await message.reply(text=text)
