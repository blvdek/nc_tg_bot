from aiogram.types import Message
from nc_py_api import AsyncNextcloud

from bot.keyboards import FilesMenuBoard
from bot.language import LocalizedTranslator
from bot.utils.nextcloud import FileManager


async def menu(message: Message, translator: LocalizedTranslator, nc: AsyncNextcloud) -> None:
    fm = await FileManager.create_root_instance(nc)

    text = translator.get("file", name=fm.file.name)
    reply_markup = FilesMenuBoard(
        translator=translator,
        author_id=message.from_user.id,
        file=fm.file,
        files=await fm.listdir(),
    ).get_kb()
    await message.reply(text=text, reply_markup=reply_markup)
