from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard, reply_board
from bot.keyboards.callback_data_factories import FilesData
from bot.language import LocalizedTranslator
from bot.states import FilesMenuStatesGroup
from bot.utils.nextcloud import FileManager


async def start_mkdir(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: FilesData,
    translator: LocalizedTranslator,
) -> None:
    await state.set_state(FilesMenuStatesGroup.MKDIR)
    await state.update_data(file_id=callback_data.file_id)

    text = translator.get("file-mkdir-description")
    await query.message.edit_text(text=text, reply_markup=None)

    reply_markup = reply_board(
        translator.get("cancel-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    text = translator.get("file-mkdir-start")
    await query.message.answer(text=text, reply_markup=reply_markup)

    await query.answer()


async def mkdir(
    message: Message,
    state: FSMContext,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    data = await state.get_data()

    fm = await FileManager.create_instance_by_id(nc, data["file_id"])
    if fm is None:
        await message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    await fm.mkdir(message.text)

    reply_markup = reply_board(
        translator.get("files-menu-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    text = translator.get("file-mkdir-success")
    await message.reply(text=text, reply_markup=reply_markup)

    await state.clear()

    text = translator.get("file", name=fm.file.name)
    files_menu_reply_markup = FilesMenuBoard(
        translator,
        author_id=message.from_user.id,
        file=fm.file,
        files=await fm.listdir(),
    ).get_kb()
    await message.reply(text=text, reply_markup=files_menu_reply_markup)


async def incorrectly_mkdir(message: Message, translator: LocalizedTranslator) -> None:
    text = translator.get("file-mkdir-incorrectly")
    await message.reply(text=text)
