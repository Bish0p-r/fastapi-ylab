from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base.model import BaseModel

if TYPE_CHECKING:
    from app.models.submenu import SubMenu


class Dish(BaseModel):
    __tablename__ = 'dishes'
    __table_args__ = (UniqueConstraint('submenu_id', 'title'),)

    price: Mapped[DECIMAL] = mapped_column(DECIMAL(scale=2), nullable=False)

    submenu_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('submenus.id', ondelete='CASCADE'), nullable=False)
    submenu: Mapped[list['SubMenu']] = relationship('SubMenu', back_populates='dishes')
