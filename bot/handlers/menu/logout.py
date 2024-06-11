from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from nc_py_api import AsyncNextcloud

from bot.db import UnitOfWork
from bot.keyboards import logout_board
from bot.language import LocalizedTranslator


async def logout(message: Message, translator: LocalizedTranslator) -> None:
    text = translator.get("logout")
    reply_markup = logout_board(translator)
    await message.answer(text=text, reply_markup=reply_markup)


async def logout_confirm(
    query: CallbackQuery,
    state: FSMContext,
    nc: AsyncNextcloud,
    uow: UnitOfWork,
    translator: LocalizedTranslator,
) -> None:
    await nc.ocs("DELETE", "/ocs/v2.php/core/apppassword")
    await uow.users.delete(query.from_user.id)
    await uow.commit()

    await state.clear()

    text = translator.get("logout-confirm")
    await query.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await query.message.delete()
    await query.answer()


async def logout_cancel(
    query: CallbackQuery,
    translator: LocalizedTranslator,
) -> None:
    text = translator.get("logout-cancel")
    await query.message.edit_text(text=text, reply_markup=None)
