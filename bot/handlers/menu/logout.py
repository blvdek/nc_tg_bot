
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.db import UnitOfWork
from bot.handlers._core import get_query_msg
from bot.keyboards import logout_board


async def logout(message: Message, i18n: I18nContext) -> None:
    text = i18n.get("logout")
    reply_markup = logout_board()
    await message.answer(text=text, reply_markup=reply_markup)


@get_query_msg
async def logout_confirm(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
    uow: UnitOfWork,
) -> None:
    await nc.ocs("DELETE", "/ocs/v2.php/core/apppassword")
    await uow.users.delete(query.from_user.id)
    await uow.commit()

    await state.clear()

    text = i18n.get("logout-confirm")
    await query_msg.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await query_msg.edit_reply_markup(None)
    await query.answer()


@get_query_msg
async def logout_cancel(query: CallbackQuery, query_msg: Message, i18n: I18nContext) -> None:
    text = i18n.get("logout-cancel")
    await query_msg.edit_text(text=text, reply_markup=None)
