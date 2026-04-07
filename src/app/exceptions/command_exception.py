class IncorrectRequestCommandError(Exception):
    def __init__(self):
        super().__init__("El dispositivo no acepta los comandos correspondiente")
