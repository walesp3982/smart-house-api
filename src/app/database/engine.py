import logging

from sqlalchemy import Engine, create_engine

from app.settings import general_settings, get_logger_path, get_url_database

# Configuracion del logger del engine


# Solo los logs de SQLAlchemy van al archivo
def _setup_logger():
    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.setLevel(logging.INFO)
    handler = logging.FileHandler(get_logger_path("sql_queries.log"))
    handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    sql_logger.addHandler(handler)


def get_engine() -> Engine:
    _setup_logger()
    return create_engine(get_url_database(), echo=general_settings.sql_debug)
