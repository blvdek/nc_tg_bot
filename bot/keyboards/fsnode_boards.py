from typing import Any

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup
from nc_py_api.files import FsNode

from bot.keyboards.callback_data_factories import FsNodeData, FsNodeMenuActions, FsNodeMenuData
from bot.keyboards.fsnode_board_abstract import FsNodeBaseBoard


class FsNodeMenuBoard(FsNodeBaseBoard):
    fsnode_callback_data = FsNodeData
    actions_callback_data = FsNodeMenuData
    actions = FsNodeMenuActions

    def __init__(
        self,
        fsnode: FsNode,
        attached_fsnodes: list[FsNode],
        from_user_id: int,
        **kwargs: Any,
    ) -> None:
        self.fsnode = fsnode
        super().__init__(
            attached_fsnodes,
            from_user_id,
            **kwargs,
            file_id=self.fsnode.file_id,
        )

    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        if self.fsnode.user_path != "" and self.fsnode.is_deletable:
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-delete-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.DELETE,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                        from_user_id=self.from_user_id,
                    ).pack(),
                ),
            )
        if not self.fsnode.is_dir:
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-download-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.DOWNLOAD,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                        from_user_id=self.from_user_id,
                    ).pack(),
                ),
            )
        if self.fsnode.is_dir and self.fsnode.is_creatable:
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-upload-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.UPLOAD,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                        from_user_id=self.from_user_id,
                    ).pack(),
                ),
            )
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-mkdir-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.MKDIR,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                        from_user_id=self.from_user_id,
                    ).pack(),
                ),
            )
        if self.fsnode.user_path != "":
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-back-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.BACK,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                        from_user_id=self.from_user_id,
                    ).pack(),
                ),
            )
        builder.adjust(1)
        return builder


def fsnode_delete_board(
    fsnode: FsNode,
    from_user_id: int,
    page: int = 0,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("confirm-button"),
                    callback_data=FsNodeMenuData(
                        action=FsNodeMenuActions.DELETE_CONFIRM,
                        page=page,
                        file_id=fsnode.file_id,
                        from_user_id=from_user_id,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=LazyProxy("deny-button"),
                    callback_data=FsNodeMenuData(
                        action=FsNodeMenuActions.CANCEL,
                        page=page,
                        file_id=fsnode.file_id,
                        from_user_id=from_user_id,
                    ).pack(),
                ),
            ],
        ],
    )
