from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from nc_py_api import AsyncNextcloud

from bot.core.config import settings
from bot.keyboards import reply_board
from bot.keyboards.callback_data_factories import FilesData
from bot.language import LocalizedTranslator
from bot.states import FilesMenuStatesGroup
from bot.utils.nextcloud import FileManager


async def upload_start(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: FilesData,
    translator: LocalizedTranslator,
) -> None:
    await state.set_state(FilesMenuStatesGroup.UPLOAD)
    await state.update_data(file_id=callback_data.file_id)

    text = translator.get("file-upload-description")
    await query.message.edit_text(text=text, reply_markup=None)

    reply_markup = reply_board(
        translator.get("stop-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    text = translator.get("file-upload-start")
    await query.message.answer(text=text, reply_markup=reply_markup)

    await query.answer()


async def upload(
    message: Message,
    bot: Bot,
    state: FSMContext,
    translator: LocalizedTranslator,
    nc: AsyncNextcloud,
) -> None:
    data = await state.get_data()

    fm = await FileManager.create_instance_by_id(nc, data["file_id"])
    if fm is None:
        await message.edit_text(text=translator.get("file-not-found"), reply_markup=None)
        return

    tg_file_obj = await bot.get_file(message.document.file_id)
    buff = await bot.download_file(tg_file_obj.file_path, chunk_size=settings.telegram.chunk_size)
    await fm.upload(buff, message.document.file_name)

    text = translator.get("file-upload-success")
    await message.reply(text=text)


async def upload_incorrectly(message: Message, translator: LocalizedTranslator) -> None:
    text = translator.get("file-upload-incorrectly")
    await message.reply(text=text)
