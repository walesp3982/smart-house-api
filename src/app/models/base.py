import logging

from sqlalchemy import Engine, MetaData, create_engine

from app.settings import (
    AvailableDatabases,
    database_settings,
    general_settings,
    get_logger_path,
)

# configuracion del logger del engine


# Creación de folder de logs si no existe

# Solo los logs de SQLAlchemy van al archivo
sql_logger = logging.getLogger("sqlalchemy.engine")
sql_logger.setLevel(logging.INFO)

handler = logging.FileHandler(get_logger_path("sql_queries.log"))
handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))


type_db = database_settings.type
match type_db:
    case AvailableDatabases.mysql:
        # ? MODIFICAR ESTAS LINEAS SI SE USAN MAS DB'S
        host = database_settings.host
        port = database_settings.port
        user = database_settings.user
        password = database_settings.password
        name_db = database_settings.name_db
        # ? HASTA AQUÍ
        connection = f"{type_db}+pymysql://{user}:{password}@{host}:{port}/{name_db}"
        # * Usando pymysql como driver del engine con mysql

    case AvailableDatabases.sqlite:
        # Guardamos en la db
        connection = "sqlite:///app.sqlite"
        # * Usando sqlite como base de datos

engine: Engine = create_engine(connection, echo=general_settings.sql_debug)
sql_logger.addHandler(handler)
metadata = MetaData()
