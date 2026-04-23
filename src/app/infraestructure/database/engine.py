from sqlalchemy import Engine, create_engine

from app.settings import general_settings, get_url_database

# Configuracion del logger del engine
_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_url_database(),
            echo=general_settings.sql_debug,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_pre_ping=True,
            pool_recycle=1800,
        )
    return _engine


def dispose_engine() -> None:
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None
