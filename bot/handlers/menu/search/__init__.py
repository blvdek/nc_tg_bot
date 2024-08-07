"""Router with search messages."""

from aiogram import F, Router
from aiogram_i18n import LazyFilter

from .pag import pag
from .search import search, start_search
from .select import select
from bot.filters import AuthorizedFilter, OnlyPrivateFilter
from bot.keyboards.callback_data_factories import SearchActions, SearchData, SearchFsNodeData
from bot.states import SearchStatesGroup


def search_router() -> Router:
    """Build router with search messages.

    :return: Router with search messages.
    """
    router = Router()

    router.message.register(
        start_search,
        LazyFilter("search-button"),
        AuthorizedFilter(),
        OnlyPrivateFilter(),
    )
    router.message.register(search, SearchStatesGroup.SEARCH)

    router.callback_query.register(
        pag,
        SearchData.filter(F.action.in_({SearchActions.PAG_BACK, SearchActions.PAG_NEXT})),
    )

    router.callback_query.register(select, SearchFsNodeData.filter())

    return router
