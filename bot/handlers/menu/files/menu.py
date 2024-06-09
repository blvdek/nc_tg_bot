from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard
from bot.language import LocalizedTranslator
from bot.nextcloud import FileManager
from bot.states import FilesMenuStatesGroup


async def menu(message: Message, state: FSMContext, translator: LocalizedTranslator, nc: AsyncNextcloud) -> None:
    await state.clear()
    await state.set_state(FilesMenuStatesGroup.DEFAULT)

    fm = await FileManager.create_root_instance(nc)

    text = translator.get("file", name=fm.file.name)
    reply_markup = FilesMenuBoard(translator=translator, file=fm.file, files=await fm.listdir())
    menu_msg = await message.reply(text=text, reply_markup=reply_markup())

    await state.update_data(menu_msg_id=menu_msg.message_id)
