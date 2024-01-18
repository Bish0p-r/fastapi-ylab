from app.repositories.menu import MenuRepository


class MenuServices:
    def __init__(self, repository: type[MenuRepository]):
        self.repository = repository
