from typing import cast

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg, validate_query_msg
from bot.keyboards.callback_data_factories import SearchFsNodeData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError


@validate_query_msg
async def select(
    query: CallbackQuery,
    callback_data: SearchFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    query_msg = cast(Message, query.message)

    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, query.from_user.id)
    await query_msg.reply(text=text, reply_markup=reply_markup)

    await query.answer()
