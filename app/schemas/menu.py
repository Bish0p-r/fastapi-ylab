from app.common.base.schema import BaseCreateSchema, BaseSchema
from app.schemas.submenu import SubMenuTreeSchema


class MenuSchema(BaseSchema):
    ...


class MenuWithCountsSchema(BaseSchema):
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCreateSchema(BaseCreateSchema):
    ...


class MenuUpdateSchema(BaseCreateSchema):
    ...


class MenuTreeSchema(MenuSchema):
    submenus: list[SubMenuTreeSchema]
