"""Download fsnode handler."""

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.handlers._core import get_human_readable_bytes, get_query_msg
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError


@get_query_msg
async def download(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Downloads a file from Nextcloud server.

    If the file is larger than the specified size, then a link will be sent, which will be valid for 8 hours.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    if srv.fsnode.info.size == 0:
        text = i18n.get("fsnode-empty")
        await query.answer(text=text)
        return
    if srv.fsnode.info.size > settings.tg.max_upload_size:
        text = i18n.get(
            "fsnode-size-limit",
            size=get_human_readable_bytes(srv.fsnode.info.size),
            size_limit=get_human_readable_bytes(settings.tg.max_upload_size),
        )
        await query.answer(text=text)
        return

    await query_msg.answer_document(await srv.download())
    await query.answer()
