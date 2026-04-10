class DatabaseConstraintException(Exception):
    def __init__(self, text: str) -> None:
        super().__init__(text)