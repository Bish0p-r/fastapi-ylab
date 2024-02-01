from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base.model import BaseModel

if TYPE_CHECKING:
    from app.models.submenu import SubMenu


class Menu(BaseModel):
    __tablename__ = 'menus'

    title: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    submenus: Mapped[list['SubMenu']] = relationship('SubMenu', back_populates='menu', cascade='delete')
