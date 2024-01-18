from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.menu import Menu
    from app.models.dish import Dish


class SubMenu(BaseModel):
    __tablename__ = "submenus"

    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id"), nullable=False)

    menu: Mapped["Menu"] = relationship(back_populates="submenu")
    dishes: Mapped[List["Dish"]] = relationship(back_populates='submenu', cascade="all, delete")
