from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard
from bot.keyboards.callback_data_factories import FilesMenuActions, FilesMenuData
from bot.language import LocalizedTranslator
from bot.nextcloud import FileManager


async def pag(
    query: CallbackQuery,
    translator: LocalizedTranslator,
    callback_data: FilesMenuData,
    nc: AsyncNextcloud,
) -> None:
    page_num = int(callback_data.page)
    page = page_num + 1 if callback_data.action == FilesMenuActions.PAG_NEXT else page_num - 1

    fm = await FileManager.create_instance_by_id(nc, callback_data.file_id)
    if fm is None:
        await query.message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    reply_markup = FilesMenuBoard(translator, file=fm.file, files=await fm.listdir(), page=page)
    with suppress(TelegramBadRequest):
        await query.message.edit_reply_markup(reply_markup=reply_markup())
    await query.answer()
