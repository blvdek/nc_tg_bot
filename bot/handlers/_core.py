from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, NotRequired, ParamSpec, TypedDict, TypeVar, Unpack

from aiogram.types import CallbackQuery, Document, InlineKeyboardMarkup, Message
from aiogram_i18n import I18nContext
from nc_py_api import FsNode

from bot.core import settings
from bot.keyboards import FsNodeMenuBoard, SearchBoard, TrashbinBoard
from bot.utils import MIME_SYMBOLS

P = ParamSpec("P")
R = TypeVar("R")


def get_msg_text(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    """Update message handler with message text argument.

    Extracts text from a message and updates the keyword arguments with the extracted text if this text exists,
    else handler will not be called.
    """

    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        message = args[0]
        if not isinstance(message, Message):
            return None

        if not isinstance(message.text, str):
            msg = "The message does not contain text."
            raise TypeError(msg)

        kwargs.update({"msg_text": message.text})
        return await f(*args, **kwargs)

    return wrapper


def get_msg_doc(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    """Update message handler with message document argument.

    Extracts a document from a message and updates the keyword arguments with the extracted document if document exists,
    else handler will not be called.
    """

    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        message = args[0]
        if not isinstance(message, Message):
            return None

        if not isinstance(message.document, Document):
            msg = "The message does not contain document."
            raise TypeError(msg)

        kwargs.update({"msg_doc": message.document})
        return await f(*args, **kwargs)

    return wrapper


def get_msg_user(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    """Update mesage handler with message sender argument.

    Extracts the sender of a message from the message and updates the keyword arguments with the sender
    if sender is accessible, else handler will not be called.
    """

    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        message = args[0]
        if not isinstance(message, Message):
            return None

        if message.from_user is None:
            msg = "Sender of this message not found."
            raise ValueError(msg)

        kwargs.update({"msg_from_user": message.from_user})
        return await f(*args, **kwargs)

    return wrapper


def get_query_msg(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    """Update callback query handler with query message argument.

    Extracts query message from the callback and updates the keyword arguments with the query message
    if query message is accessible, else handler will not be called and a message will be sent to the user
    that the request message is inaccessible.
    """

    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        query = args[0]
        if not isinstance(query, CallbackQuery):
            return None

        if not isinstance(query.message, Message):
            i18n = kwargs.get("i18n")
            if not isinstance(i18n, I18nContext):
                msg = "i18n context is required but was not provided."
                raise TypeError(msg)
            text = i18n.get("msg-is-inaccessible")
            await query.answer(text)
            return None

        kwargs.update({"query_msg": query.message})
        return await f(*args, **kwargs)

    return wrapper


def get_human_readable_bytes(num: float, suffix: str = "B") -> str:
    """A function that convert a number of bytes into a human-readable format.

    :param num: The number of bytes to convert.
    :param suffix: The suffix to append to the converted value, defaults to "B".
    :return: A human-readable string representing the converted byte value with the appropriate unit.
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 2**10:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 2**10
    return f"{num:.1f}Yi{suffix}"


def get_page_items(item_list: list[R], page: int = 0, page_size: int = settings.telegram.page_size) -> list[R]:
    """Return a slice of the input list `item_list` based on the provided `page` and `page_size`.

    :param item_list: The list from which to extract the items.
    :param page: The page number to retrieve. Defaults to 0.
    :param page_size: The number of items per page, defaults to the value of `settings.telegram.page_size`.
    :return: A list containing the items on the specified page.
    """
    start_index = page * page_size
    end_index = (page + 1) * page_size
    return item_list[start_index:end_index]


def get_fsnode_msg(
    i18n: I18nContext,
    fsnode: FsNode,
    attached_fsnodes: list[FsNode],
    from_user_id: int,
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup]:
    text = i18n.get(
        "fsnode",
        type="dir" if fsnode.is_dir else "file",
        symbol="📂" if fsnode.is_dir else MIME_SYMBOLS.get(fsnode.info.mimetype, ""),
        name=fsnode.name,
        path=fsnode.user_path if fsnode.user_path else "/",
        user=fsnode.user,
        favorite="🌕" if fsnode.info.favorite else "🌑",
        size=get_human_readable_bytes(fsnode.info.size),
        last_modified=fsnode.info.last_modified,
    )
    reply_markup = FsNodeMenuBoard(
        fsnode=fsnode,
        attached_fsnodes=attached_fsnodes,
        from_user_id=from_user_id,
        **kwargs,
    ).get_kb()
    return text, reply_markup


def get_trashbin_msg(
    i18n: I18nContext,
    trashbin: list[FsNode],
    trashbin_size: int,
    from_user_id: int,
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup | None]:
    if trashbin == []:
        text = i18n.get("trashbin-empty")
        return text, None
    fsnodes_on_page = get_page_items(trashbin, **kwargs)
    fsnodes_text = "\n".join(
        [
            i18n.get(
                "trashbin-item",
                path=fsnode.info.trashbin_original_location if fsnode.info.trashbin_original_location else "/",
            )
            for fsnode in fsnodes_on_page
        ],
    )
    text = f"{i18n.get('trashbin', count=len(trashbin), size=get_human_readable_bytes(trashbin_size))}\n{fsnodes_text}"
    reply_markup = TrashbinBoard(
        fsnodes=trashbin,
        from_user_id=from_user_id,
        **kwargs,
    ).get_kb()
    return text, reply_markup


class GetSeachMsgArgs(TypedDict):
    page: NotRequired[int]
    page_size: NotRequired[int]


def get_search_msg(
    i18n: I18nContext,
    query: str,
    fsnodes: list[FsNode],
    from_user_id: int,
    **kwargs: Unpack[GetSeachMsgArgs],
) -> tuple[str, InlineKeyboardMarkup | None]:
    if fsnodes == []:
        text = i18n.get("search-empty")
        return text, None
    fsnodes_on_page = get_page_items(fsnodes, **kwargs)
    fsnodes_text = "\n".join(
        [i18n.get("search-item", path=fsnode.user_path if fsnode.user_path else "/") for fsnode in fsnodes_on_page],
    )
    text = f"{i18n.get('search', count=len(fsnodes), query=query)}\n{fsnodes_text}"
    reply_markup = SearchBoard(
        query=query,
        fsnodes=fsnodes,
        from_user_id=from_user_id,
        **kwargs,
    ).get_kb()
    return text, reply_markup
