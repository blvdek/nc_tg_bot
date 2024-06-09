from aiogram.fsm.state import State, StatesGroup


class FilesMenuStatesGroup(StatesGroup):
    DEFAULT = State()
    UPLOAD = State()
    MKDIR = State()
