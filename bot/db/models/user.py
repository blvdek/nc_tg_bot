from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    nc_login: Mapped[str] = mapped_column(nullable=False)
    nc_app_password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
