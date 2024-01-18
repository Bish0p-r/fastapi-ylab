from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.menu import Menu
    from app.models.dish import Dish


class SubMenu(BaseModel):
    __tablename__ = "submenus"

    menu_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('menus.id', ondelete='CASCADE'), nullable=False)

    menu: Mapped[list['Menu']] = relationship('Menu', back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='submenu', cascade='delete')
