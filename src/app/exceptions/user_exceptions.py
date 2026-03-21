class EmailAlreadyRegisterError(Exception):
    def __init__(self):
        super().__init__("El email ya fue registrado anteriormente")


class UserNotFoundError(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"User with id:{id} not found")


class CredencialsUserIncorrectError(Exception):
    def __init__(self) -> None:
        super().__init__("La credenciales proporcionadas son incorrectas")


class UserNotFoundByEmailError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"No se encontró el usuario con email {email}")


class UserNotCreatedError(Exception):
    def __init__(self) -> None:
        super().__init__("El usuario no ha podido ser creado")


class UserNotFoundByIdError(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"No se encontró el usuario con id {id}")


class UserNotFoundByToken(Exception):
    def __init__(self) -> None:
        super().__init__("Usuario no encontrado")


class VerificationEmailInvalid(Exception):
    def __init__(self) -> None:
        super().__init__("Verificación de email inválida")
