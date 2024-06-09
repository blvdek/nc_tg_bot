from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from nc_py_api import AsyncNextcloud

from bot.db import UnitOfWork
from bot.keyboards import logout_board
from bot.language import LocalizedTranslator


async def logout(message: Message, translator: LocalizedTranslator) -> None:
    await message.answer(text=translator.get("logout"), reply_markup=logout_board(translator))


async def logout_confirm(
    query: CallbackQuery,
    state: FSMContext,
    nc: AsyncNextcloud,
    db: UnitOfWork,
    translator: LocalizedTranslator,
) -> None:
    await nc.ocs("DELETE", "/ocs/v2.php/core/apppassword")
    await db.users.delete(query.from_user.id)
    await db.commit()

    await state.clear()
    await query.message.reply(text=translator.get("logout-confirm"), reply_markup=ReplyKeyboardRemove())
    await query.message.delete()
    await query.answer()


async def logout_cancel(
    query: CallbackQuery,
    translator: LocalizedTranslator,
) -> None:
    await query.message.edit_text(translator.get("logout-cancel"), reply_markup=None)
