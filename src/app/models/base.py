import logging

from sqlalchemy import Engine, MetaData, create_engine

from app.settings import (
    general_settings,
    get_logger_path,
    get_url_database,
)

# Configuracion del logger del engine

# Solo los logs de SQLAlchemy van al archivo
sql_logger = logging.getLogger("sqlalchemy.engine")
sql_logger.setLevel(logging.INFO)

handler = logging.FileHandler(get_logger_path("sql_queries.log"))
handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))


# Creamos la conexion a la base de datos
connection = get_url_database
engine: Engine = create_engine(get_url_database, echo=general_settings.sql_debug)
sql_logger.addHandler(handler)
metadata = MetaData()
