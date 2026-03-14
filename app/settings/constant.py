from pathlib import Path


def get_logger_path(filename: str) -> str:
    return f"{FOLDER_LOGGER}/{filename}"


def create_folder_logger():
    folder_path = Path(FOLDER_LOGGER)
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)


FOLDER_LOGGER = "logs"
create_folder_logger()
