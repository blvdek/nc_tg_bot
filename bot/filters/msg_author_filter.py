from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, TelegramObject
from aiogram_i18n import I18nContext


class MsgAuthorFilter(BaseFilter):
    def __init__(self, callback_data: type[CallbackData]):
        self.callback_data = callback_data

    async def __call__(self, event: TelegramObject, i18n: I18nContext) -> bool:
        if not isinstance(event, CallbackQuery):
            msg = "'MsgAuthorFilter' works only with 'CallbackQuery'."
            raise TypeError(msg)
        if event.data is None:
            msg = "'CallbackData' is not specified in 'CallbackQuery'."
            raise RuntimeError(msg)
        data = self.callback_data.unpack(event.data)

        if not hasattr(data, "from_user_id"):
            raise RuntimeError

        if data.from_user_id == event.from_user.id:
            return True

        await event.answer(text=i18n.get("not_author"))
        return False
