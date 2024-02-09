from app.repositories.dish import DishRepository
from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubMenuRepository
from app.services.admin import AdminServices
from app.services.cache import cache_service

admin_services = AdminServices(MenuRepository, SubMenuRepository, DishRepository, cache_service)
