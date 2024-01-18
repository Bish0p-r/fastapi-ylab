from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.menu import Menu


class SubMenu(BaseModel):
    __tablename__ = "submenus"

    menu_id: Mapped[UUID] = mapped_column(ForeignKey("menus.id"), nullable=False)
    menu: Mapped[List["Menu"]] = relationship(back_populates="submenus")
