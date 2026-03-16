import logging

from sqlalchemy import Engine, MetaData, create_engine

from app.settings import (
    general_settings,
    get_logger_path,
    get_url_database,
)

# configuracion del logger del engine


# Creación de folder de logs si no existe

# Solo los logs de SQLAlchemy van al archivo
sql_logger = logging.getLogger("sqlalchemy.engine")
sql_logger.setLevel(logging.INFO)

handler = logging.FileHandler(get_logger_path("sql_queries.log"))
handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))


connection = get_url_database
engine: Engine = create_engine(get_url_database, echo=general_settings.sql_debug)
sql_logger.addHandler(handler)
metadata = MetaData()
