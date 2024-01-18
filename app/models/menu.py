from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.submenu import SubMenu


class Menu(BaseModel):
    __tablename__ = "menus"

    submenus: Mapped[List["SubMenu"]] = relationship("SubMenu", back_populates="menu", cascade="all, delete")
