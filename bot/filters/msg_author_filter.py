
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, TelegramObject

from bot.keyboards.callback_data_factories import FilesData
from bot.language import LocalizedTranslator


class MsgAuthorFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, translator: LocalizedTranslator) -> bool:
        if not isinstance(event, CallbackQuery):
            msg = "MsgAuthorFilter works only with CallbackQuery."
            raise TypeError(msg)
        if event.data is None:
            msg = ""
            raise RuntimeError(msg)
        data = FilesData.unpack(event.data)

        if data.author_id == event.from_user.id:
            return True

        await event.answer(text=translator.get("not_author"))
        return False
