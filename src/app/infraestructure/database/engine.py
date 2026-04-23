from sqlalchemy import Engine, create_engine

from app.settings import general_settings, get_url_database

# Configuracion del logger del engine


def get_engine() -> Engine:
    return create_engine(get_url_database(), echo=general_settings.sql_debug)
