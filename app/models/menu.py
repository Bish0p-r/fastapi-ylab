from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.submenu import SubMenu
    from app.models.dish import Dish


class Menu(BaseModel):
    __tablename__ = "menus"

    title: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    submenus: Mapped[list['SubMenu']] = relationship('SubMenu', back_populates='menu', cascade='delete')
