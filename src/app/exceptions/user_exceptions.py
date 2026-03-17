

class UserNotFoundException(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"User with id:{id} not found")

