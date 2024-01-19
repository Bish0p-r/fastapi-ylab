from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.menu import Menu
    from app.models.dish import Dish


class SubMenu(BaseModel):
    __tablename__ = "submenus"
    __table_args__ = (UniqueConstraint("menu_id", "title"),)

    menu_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False)

    menu: Mapped[list["Menu"]] = relationship("Menu", back_populates="submenus")
    dishes: Mapped[list["Dish"]] = relationship("Dish", back_populates="submenu", cascade="delete")
