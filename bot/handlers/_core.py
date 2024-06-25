from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, User
from aiogram_i18n import I18nContext
from nc_py_api import FsNode

from bot.keyboards import FsNodeMenuBoard, SearchBoard, TrashbinBoard

P = ParamSpec("P")
R = TypeVar("R")


def validate_msg_text(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        message = args[0]
        if not isinstance(message, Message):
            return None
        if not isinstance(message.text, str):
            return None
        return await f(*args, **kwargs)

    return wrapper


def validate_msg_user(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        message = args[0]
        if not isinstance(message, Message):
            return None
        if not isinstance(message.from_user, User):
            return None
        return await f(*args, **kwargs)

    return wrapper


def validate_query_msg(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        query = args[0]
        if not isinstance(query, CallbackQuery):
            return None
        if not isinstance(query.message, Message):
            return None
        return await f(*args, **kwargs)

    return wrapper


def get_fsnode_msg(
    i18n: I18nContext,
    fsnode: FsNode,
    attached_fsnodes: list[FsNode],
    from_user_id: int,
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup]:
    text = i18n.get("fsnode", name=fsnode.name)
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
    from_user_id: int,
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup | None]:
    if trashbin == []:
        text = i18n.get("trashbin-empty")
        return text, None
    text = i18n.get("trashbin")
    reply_markup = TrashbinBoard(
        fsnodes=trashbin,
        from_user_id=from_user_id,
        **kwargs,
    ).get_kb()
    return text, reply_markup


def get_search_msg(
    i18n: I18nContext,
    query: str,
    fsnodes: list[FsNode],
    from_user_id: int,
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup | None]:
    if fsnodes == []:
        text = i18n.get("search-empty")
        return text, None
    text = i18n.get("search")
    reply_markup = SearchBoard(
        query=query,
        fsnodes=fsnodes,
        from_user_id=from_user_id,
        **kwargs,
    ).get_kb()
    return text, reply_markup
