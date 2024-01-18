from app.repositories.dish import DishRepository


class DishServices:
    def __init__(self, repository: type[DishRepository]):
        self.repository = repository
