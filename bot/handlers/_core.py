from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, NotRequired, ParamSpec, TypedDict, TypeVar, Unpack

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, User
from aiogram_i18n import I18nContext
from nc_py_api import FsNode

from bot.core import settings
from bot.keyboards import FsNodeMenuBoard, SearchBoard, TrashbinBoard
from bot.utils import MIME_SYMBOLS

P = ParamSpec("P")
R = TypeVar("R")


def get_msg_text(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
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


def get_msg_user(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        message = args[0]
        if not isinstance(message, Message):
            return None

        if message.from_user is None:
            msg = "Sender of this message not found."
            raise ValueError(msg)

        kwargs.update({"msg_user": message.from_user})
        return await f(*args, **kwargs)

    return wrapper


def get_query_msg(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
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
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 2**10:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 2**10
    return f"{num:.1f}Yi{suffix}"


def get_page_items(item_list: list[R], page: int = 0, page_size: int = settings.telegram.page_size) -> list[R]:
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
