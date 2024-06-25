from typing import cast

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.db import UnitOfWork
from bot.handlers._core import validate_query_msg
from bot.keyboards import logout_board


async def logout(message: Message, i18n: I18nContext) -> None:
    text = i18n.get("logout")
    reply_markup = logout_board()
    await message.answer(text=text, reply_markup=reply_markup)


@validate_query_msg
async def logout_confirm(
    query: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
    uow: UnitOfWork,
) -> None:
    query_msg = cast(Message, query.message)

    await nc.ocs("DELETE", "/ocs/v2.php/core/apppassword")
    await uow.users.delete(query.from_user.id)
    await uow.commit()

    await state.clear()

    text = i18n.get("logout-confirm")
    await query_msg.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await query_msg.delete()
    await query.answer()


@validate_query_msg
async def logout_cancel(query: CallbackQuery, i18n: I18nContext) -> None:
    query_msg = cast(Message, query.message)

    text = i18n.get("logout-cancel")
    await query_msg.edit_text(text=text, reply_markup=None)
