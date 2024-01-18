from app.repositories.submenu import SubMenuRepository


class SubMenuServices:
    def __init__(self, repository: type[SubMenuRepository]):
        self.repository = repository
