from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard
from bot.keyboards.callback_data_factories import FilesActions, FilesData
from bot.language import LocalizedTranslator
from bot.utils.nextcloud import FileManager


async def pag(
    query: CallbackQuery,
    translator: LocalizedTranslator,
    callback_data: FilesData,
    nc: AsyncNextcloud,
) -> None:
    page_num = int(callback_data.page)
    page = page_num + 1 if callback_data.action == FilesActions.PAG_NEXT else page_num - 1

    fm = await FileManager.create_instance_by_id(nc, callback_data.file_id)
    if fm is None:
        await query.message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    reply_markup = FilesMenuBoard(
        translator=translator,
        author_id=query.from_user.id,
        file=fm.file,
        files=await fm.listdir(),
        page=page,
    ).get_kb()
    with suppress(TelegramBadRequest):
        await query.message.edit_reply_markup(reply_markup=reply_markup)
    await query.answer()
