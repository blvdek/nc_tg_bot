from aiogram.fsm.state import State, StatesGroup


class FilesMenuStatesGroup(StatesGroup):
    UPLOAD = State()
    MKDIR = State()
