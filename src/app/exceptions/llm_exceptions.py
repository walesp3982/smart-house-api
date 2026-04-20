class LLMResponseNotCreated(Exception):
    def __init__(self) -> None:
        super().__init__("No se puedo generar la respuesta")
