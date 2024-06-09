from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard
from bot.keyboards.callback_data_factories import FilesMenuData
from bot.language import LocalizedTranslator
from bot.nextcloud import FileManager


async def back(
    query: CallbackQuery,
    callback_data: FilesMenuData,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    fm = await FileManager.create_prev_instance_by_id(nc, callback_data.file_id)
    if fm is None:
        await query.message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    files = await fm.listdir()

    text = translator.get("file", name=fm.file.name)
    reply_markup = FilesMenuBoard(translator=translator, file=fm.file, files=files)

    with suppress(TelegramBadRequest):
        await query.message.edit_text(text=text, reply_markup=reply_markup())

    await query.answer()
