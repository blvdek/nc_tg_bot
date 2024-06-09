from aiogram.types import CallbackQuery
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.keyboards.callback_data_factories import FilesMenuData
from bot.language import LocalizedTranslator
from bot.nextcloud import FileManager


async def download(
    query: CallbackQuery,
    callback_data: FilesMenuData,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    fm = await FileManager.create_instance_by_id(nc, callback_data.file_id)
    if fm is None:
        await query.message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    if fm.file.info.size > settings.telegram.max_upload_size or fm.file.info.size == 0:
        await query.message.answer(await fm.direct_download())
        await query.answer()
        return

    await query.message.answer_document(await fm.download())

    await query.answer()
