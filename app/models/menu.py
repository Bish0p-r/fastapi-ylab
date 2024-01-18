from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.submenu import SubMenu
    from app.models.dish import Dish


class Menu(BaseModel):
    __tablename__ = "menus"

    submenu: Mapped[List["SubMenu"]] = relationship(back_populates="menu", cascade="all, delete")
