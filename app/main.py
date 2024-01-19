from fastapi import APIRouter, FastAPI

from app.routes.dish import router as dish_router
from app.routes.menu import router as menu_router
from app.routes.submenu import router as submenu_router

app = FastAPI()
router = APIRouter(prefix="/api/v1")


router.include_router(menu_router)
router.include_router(submenu_router)
router.include_router(dish_router)
app.include_router(router)
