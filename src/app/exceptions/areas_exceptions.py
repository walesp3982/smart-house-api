class AreaEntityIdNotStartedError(Exception):
    def __init__(self):
        super().__init__("La entidad requiere un id para realizar la operación")


class AreaNotFoundError(Exception):
    def __init__(self):
        super().__init__("El area no fue encontrada")


class AreaNotFoundByIdError(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"No se encontró el área con id: {id}")
