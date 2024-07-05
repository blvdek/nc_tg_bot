from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.db.repositories import _Repository


class _UserRepository(_Repository[User]):
    """User repository for CRUD."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)
