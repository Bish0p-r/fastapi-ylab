from fastapi import APIRouter


router = APIRouter(
    prefix="/menus/{menu_id}/submenus",
    tags=["SubMenus"]
)