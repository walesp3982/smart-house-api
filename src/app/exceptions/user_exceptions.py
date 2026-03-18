class EmailAlreadyRegisterError(Exception):
    def __init__(self):
        super().__init__("El email ya fue registrado anteriormente")


class UserNotFoundException(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"User with id:{id} not found")


class CredencialsUserIncorrectException(Exception):
    def __init__(self) -> None:
        super().__init__("La credenciales proporcionadas son incorrectas")


class UserNotFoundByEmailException(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"No se encontró el usuario con email {email}")


class UserNotCreatedException(Exception):
    def __init__(self) -> None:
        super().__init__("El usuario no ha podido ser creado")


class UserNotFoundByIdException(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"No se encontró el usuario con id {id}")
