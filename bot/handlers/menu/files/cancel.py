from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard, menu_board
from bot.keyboards.callback_data_factories import FilesData
from bot.language import LocalizedTranslator
from bot.utils.nextcloud import FileManager


async def cancel_callback(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: FilesData,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    await state.clear()
    fm = await FileManager.create_instance_by_id(nc, callback_data.file_id)
    if fm is None:
        text = translator.get("file-not-found")
        await query.message.edit_text(text=text, reply_markup=None)
        return

    files = await fm.listdir()

    text = translator.get("file", name=fm.file.name)
    reply_markup = FilesMenuBoard(
        translator=translator,
        author_id=query.from_user.id,
        file=fm.file,
        files=files,
        page=callback_data.page,
    ).get_kb()

    await query.message.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()


async def cancel_message(
    message: Message,
    state: FSMContext,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    data = await state.get_data()

    fm = await FileManager.create_instance_by_id(nc, data["file_id"])
    if fm is None:
        text = translator.get("file-not-found")
        await message.edit_text(text=text, reply_markup=None)
        return

    await state.clear()

    reply_markup = menu_board(translator, is_persistent=True, resize_keyboard=True, selective=True)
    text = translator.get("file-cancel")
    await message.reply(text=text, reply_markup=reply_markup)

    text = translator.get("file", name=fm.file.name)
    files_menu_reply_markup = FilesMenuBoard(
        translator=translator,
        author_id=message.from_user.id,
        file=fm.file,
        files=await fm.listdir(),
    ).get_kb()
    await message.answer(text=text, reply_markup=files_menu_reply_markup)
