from typing import Optional


class HouseNotFoundError(Exception):
    def __init__(self, content: Optional[str] = None):
        text = "No se encontró la casa"
        if content is not None:
            text = content

        super().__init__(text)


class HouseNotFoundByIdError(HouseNotFoundError):
    def __init__(self, id: int) -> None:
        super().__init__(f"No se encóntro el dispositivo con id: {id}")


class HouseIdNotStarted(Exception):
    def __init__(self) -> None:
        super().__init__("No se inicializó el id del house")


class HouseCannotDeleted(Exception):
    def __init__(self) -> None:
        super().__init__("La casa no pudo elimininarse")
