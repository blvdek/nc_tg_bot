
from aiogram.types import CallbackQuery
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard, files_menu_delete_board
from bot.keyboards.callback_data_factories import FilesMenuData
from bot.language import LocalizedTranslator
from bot.nextcloud import FileManager


async def delete(
    query: CallbackQuery,
    callback_data: FilesMenuData,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    fm = await FileManager.create_instance_by_id(nc, callback_data.file_id)
    if fm is None:
        await query.message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    reply_markup = files_menu_delete_board(translator=translator, file=fm.file, page=callback_data.page)
    text = translator.get("file-delete")
    await query.message.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()


async def delete_confirm(
    query: CallbackQuery,
    callback_data: FilesMenuData,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    prev_fm = await FileManager.create_prev_instance_by_id(nc, callback_data.file_id)
    fm = await FileManager.create_instance_by_id(nc, callback_data.file_id)
    if prev_fm is None:
        await query.message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    await fm.delete()

    reply_markup = FilesMenuBoard(
        translator=translator,
        file=prev_fm.file,
        files=await prev_fm.listdir(),
        page=callback_data.page,
    )
    text = translator.get("file-delete-success")
    await query.message.edit_text(text=text, reply_markup=reply_markup())

    await query.answer(text=translator.get("file-delete-pop-up"), show_alert=True)
