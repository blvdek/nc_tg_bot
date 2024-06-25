from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Any

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton
from nc_py_api.files import FsNode

from bot.utils import MIME_SYMBOLS

DEFAULT_PAGE_SIZE = 8
FSNODE_BUTTON_TEXT_LENGTH = 32


class _FsNodeAbstractBoard(ABC):
    @abstractmethod
    def get_kb(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    @abstractmethod
    def build_fsnode_buttons(self) -> InlineKeyboardBuilder:
        raise NotImplementedError

    @abstractmethod
    def build_pag_buttons(self) -> InlineKeyboardBuilder:
        raise NotImplementedError


class FsNodeBaseBoard(_FsNodeAbstractBoard, ABC):
    fsnode_callback_data: type[CallbackData]
    actions_callback_data: type[CallbackData]
    actions: type[IntEnum]

    def __init__(
        self,
        fsnodes: list[FsNode],
        from_user_id: int,
        page: int = 0,
        page_size: int = DEFAULT_PAGE_SIZE,
        **kwargs: Any,
    ) -> None:
        self.builder = InlineKeyboardBuilder()
        self.fsnodes = sorted(fsnodes, key=lambda x: x.is_dir, reverse=True)
        self.from_user_id = from_user_id
        self.page = page
        self.page_size = page_size
        self.kwargs = kwargs

    def get_kb(self) -> InlineKeyboardMarkup:
        self.builder.attach(self.build_fsnode_buttons())
        self.builder.attach(self.build_pag_buttons())
        self.builder.attach(self.build_actions_buttons())
        return self.builder.as_markup()

    def build_fsnode_buttons(self) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()

        start_index = self.page * self.page_size
        end_index = (self.page + 1) * self.page_size

        for fsnode in self.fsnodes[start_index:end_index]:
            prefix = MIME_SYMBOLS.get(fsnode.info.mimetype, "")

            builder.button(
                text=f"{prefix} {fsnode.name[:FSNODE_BUTTON_TEXT_LENGTH]}{'/' if fsnode.is_dir else ''}",
                callback_data=self.fsnode_callback_data(
                    file_id=fsnode.file_id,
                    page=self.page,
                    from_user_id=self.from_user_id,
                ).pack(),
            )

        builder.adjust(1)
        return builder

    def build_pag_buttons(self) -> InlineKeyboardBuilder:
        if not hasattr(self.actions, "PAG_BACK") or not hasattr(self.actions, "PAG_NEXT"):
            raise RuntimeError

        builder = InlineKeyboardBuilder()

        total_fsnodes = len(self.fsnodes) - 1
        total_pages = (total_fsnodes + self.page_size - 1) // self.page_size

        if total_pages > 1:
            if self.page > 0:
                builder.add(
                    InlineKeyboardButton(
                        text=LazyProxy("fsnode-pag-back-button"),
                        callback_data=self.actions_callback_data(
                            action=self.actions.PAG_BACK,
                            page=self.page,
                            from_user_id=self.from_user_id,
                            **self.kwargs,
                        ).pack(),
                    ),
                )

            builder.button(text=f"{self.page + 1}/{total_pages}", callback_data="page")

            if total_pages - 1 > self.page:
                builder.add(
                    InlineKeyboardButton(
                        text=LazyProxy("fsnode-pag-next-button"),
                        callback_data=self.actions_callback_data(
                            action=self.actions.PAG_NEXT,
                            page=self.page,
                            from_user_id=self.from_user_id,
                            **self.kwargs,
                        ).pack(),
                    ),
                )

        builder.adjust(3)
        return builder

    @abstractmethod
    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        raise NotImplementedError
