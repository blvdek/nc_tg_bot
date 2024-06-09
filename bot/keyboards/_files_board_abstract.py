from abc import ABC, abstractmethod
from enum import IntEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from nc_py_api.files import FsNode

from bot.language import LocalizedTranslator

FILE_BUTTON_TEXT_LENGTH = 32
DEFAULT_PAGE_SIZE = 8


class _FilesBoardAbstract(ABC):
    callback_data: type[CallbackData]
    actions: type[IntEnum]

    def __init__(
        self,
        translator: LocalizedTranslator,
        file: FsNode,
        files: list[FsNode],
        page: int = 0,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> None:
        self.builder = InlineKeyboardBuilder()
        self.translator = translator
        self.file = file
        self.files = sorted(files, key=lambda x: x.is_dir, reverse=True)
        self.page = page
        self.page_size = page_size

    def __call__(self) -> InlineKeyboardMarkup:
        self.builder.attach(self._build_files_buttons())
        self.builder.attach(self._build_files_pag_buttons())
        self.builder.attach(self._build_file_actions_buttons())
        return self.builder.as_markup()

    def _build_files_buttons(self) -> InlineKeyboardBuilder:
        if not hasattr(self.actions, "SELECT"):
            msg = "'actions' must include 'SELECT' identifier."
            raise ValueError(msg)

        fb_builder = InlineKeyboardBuilder()

        start_index = self.page * self.page_size
        end_index = (self.page + 1) * self.page_size

        for file in self.files[start_index:end_index]:
            fb_builder.button(
                text=f"{file.name[:FILE_BUTTON_TEXT_LENGTH]}{'/' if file.is_dir else ''}",
                callback_data=self.callback_data(
                    action=self.actions.SELECT,
                    page=self.page,
                    file_id=file.file_id,
                ).pack(),
            )

        fb_builder.adjust(1)
        return fb_builder

    def _build_files_pag_buttons(self) -> InlineKeyboardBuilder:
        if not hasattr(self.actions, "PAG_BACK") or not hasattr(self.actions, "PAG_NEXT"):
            msg = "'actions' must include 'PAG_BACK' and 'PAG_NEXT' identifiers."
            raise ValueError(msg)

        pag_builder = InlineKeyboardBuilder()

        total_files = len(self.files) - 1
        total_pages = (total_files + self.page_size - 1) // self.page_size

        if total_pages > 1:
            if self.page > 0:
                pag_builder.button(
                    text=self.translator.get("file-pag-back-button"),
                    callback_data=self.callback_data(
                        action=self.actions.PAG_BACK,
                        page=self.page,
                        file_id=self.file.file_id,
                    ).pack(),
                )

            pag_builder.button(text=f"{self.page + 1}/{total_pages}", callback_data="page")

            if total_pages - 1 > self.page:
                pag_builder.button(
                    text=self.translator.get("file-pag-next-button"),
                    callback_data=self.callback_data(
                        action=self.actions.PAG_NEXT,
                        page=self.page,
                        file_id=self.file.file_id,
                    ).pack(),
                )

        pag_builder.adjust(3)
        return pag_builder

    @abstractmethod
    def _build_file_actions_buttons(self) -> InlineKeyboardBuilder:
        raise NotImplementedError
