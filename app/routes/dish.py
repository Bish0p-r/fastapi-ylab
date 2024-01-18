from fastapi import APIRouter


router = APIRouter(
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"]
)
