"""User model."""

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.models import Base


class User(Base):
    """User model.

    :param id: Unique Telegram identifier for the user, primary key.
    :param nc_login: The user's Nextcloud login name.
    :param nc_app_password: The user's Nextcloud app password.
    :param name: The user's name, extracted from their Telegram profile.
    :param first_name: The user's first name, extracted from their Telegram profile.
    :param last_name: The user's last name, extracted from their Telegram profile.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    nc_login: Mapped[str] = mapped_column(nullable=False)
    nc_app_password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)

    @property
    def url(self) -> str:
        """Generates a URL for the user's profile page, typically used for linking purposes."""
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        """Generates a mention string for the user, suitable for use in chat messages."""
        return html.link(value=self.name, link=self.url)
