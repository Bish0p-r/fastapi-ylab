from typing import TYPE_CHECKING, List

from sqlalchemy import DECIMAL, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base.model import BaseModel


if TYPE_CHECKING:
    from app.models.submenu import SubMenu


class Dish(BaseModel):
    __tablename__ = "dishes"

    price: Mapped[DECIMAL] = mapped_column(DECIMAL(scale=2), nullable=False)

    submenu_id: Mapped[UUID] = mapped_column(ForeignKey("submenus.id"), nullable=False)
    submenu: Mapped[List["SubMenu"]] = relationship(back_populates="dishes")
