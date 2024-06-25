from aiogram.fsm.state import State, StatesGroup


class FsNodeMenuStatesGroup(StatesGroup):
    UPLOAD = State()
    MKDIR = State()
