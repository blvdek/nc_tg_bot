from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard, reply_board
from bot.keyboards.callback_data_factories import FilesMenuData
from bot.language import LocalizedTranslator
from bot.nextcloud import FileManager
from bot.states import FilesMenuStatesGroup


async def cancel_callback(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: FilesMenuData,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    await state.set_state(FilesMenuStatesGroup.DEFAULT)
    fm = await FileManager.create_instance_by_id(nc, callback_data.file_id)
    if fm is None:
        await query.message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    files = await fm.listdir()

    text = translator.get("file", name=fm.file.name)
    reply_markup = FilesMenuBoard(translator=translator, file=fm.file, files=files, page=callback_data.page)

    await query.message.edit_text(text=text, reply_markup=reply_markup())

    await query.answer()


async def cancel_message(
    message: Message,
    state: FSMContext,
    translator: LocalizedTranslator,
) -> None:
    await state.set_state(FilesMenuStatesGroup.DEFAULT)

    reply_markup = reply_board(
        translator.get("files-menu-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    text = translator.get("file-cancel")
    await message.reply(text=text, reply_markup=reply_markup)
