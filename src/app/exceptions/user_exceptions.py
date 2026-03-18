class UserNotFoundException(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"User with id:{id} not found")


class CredencialsUserIncorrect(Exception):
    def __init__(self) -> None:
        super().__init__("La credenciales proporcionadas son incorrectas")


class UserNotFoundByEmailException(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"No se encontró el usuario con email {email}")


class UserNotCreated(Exception):
    def __init__(self) -> None:
        super().__init__("El usuario no ha podido ser creado")


class UserNotFoundByIdException(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"No se encontró el usuario con id {id}")
